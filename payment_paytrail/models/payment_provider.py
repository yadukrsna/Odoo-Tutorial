from odoo import _,models, fields
import requests
import json
import uuid
import hmac
import hashlib

from odoo.exceptions import ValidationError


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(selection_add=[("paytrail", "Paytrail")], ondelete={'paytrail': 'set default'})

    paytrail_merchant_id = fields.Char("Merchant ID", required_if_provider="paytrail")
    paytrail_secret_key = fields.Char("Merchant Secret Key", required_if_provider="paytrail")

    def _paytrail_compute_signature(self, headers: dict, body: str = '')-> str:
        self.ensure_one()
        checkout_headers = {k:v for k, v in headers.items() if k.startswith("checkout-")}
        hmac_string = [f"{key}:{value}" for key, value in sorted(checkout_headers.items())]
        hmac_string.append(body)
        hmac_str = '\n'.join(hmac_string)
        signature = hmac.new(
            self.paytrail_secret_key.encode("utf-8"),
            hmac_str.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return signature

    def create_paytrail_payment(self, transaction):
        self.ensure_one()
        currency = transaction.currency_id
        currency_eur = self.env['res.currency'].search([('name', '=', 'EUR')], limit=1)
        converted_amount = currency._convert(transaction.amount, currency_eur, self.env.company, fields.Date.today())
        amount_cents = float(converted_amount*100)
        base_url = self.get_base_url()
        payload = {
            "stamp": str(uuid.uuid4()),
            "reference": transaction.reference,
            "amount": amount_cents,
            "currency": "EUR",
            "language": "EN",
            "items": [
                {
                    "unitPrice": amount_cents,
                    "units": 1,
                    "vatPercentage": 0,
                    "productCode": transaction.reference,
                    "description": transaction.reference,
                }
            ],
            "customer": {
                "email": transaction.partner_id.email,
            },
            "redirectUrls": {
                "success": f"{base_url}/payment/paytrail/success",
                "cancel": f"{base_url}/payment/paytrail/cancel",
            }
        }
        headers = {
            "checkout-account": self.paytrail_merchant_id,
            "checkout-algorithm": "sha256",
            "checkout-method": "POST",
            "checkout-nonce": str(uuid.uuid4()),
            "checkout-timestamp": fields.Datetime.now().isoformat(),
            "content-type" : "application/json; charset=utf-8",
        }
        body = json.dumps(payload, separators=(',', ':'))
        headers["signature"] = self._paytrail_compute_signature(headers, body)
        api_url = "https://services.paytrail.com/payments"
        try:
            response = requests.post(api_url, headers=headers, data=body, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ValidationError(_("Could not connect to paytrail, %s", e))
        response_data = response.json()
        return response_data.get('href')