from odoo import http
from odoo.http import request
import logging
from werkzeug.utils import redirect


_logger = logging.getLogger(__name__)

class PaytrailController(http.Controller):

    @http.route('/payment/paytrail/redirect/<int:transaction_id>', type='http', auth='public', website=True)
    def paytrail_redirect(self, transaction_id):
        """Redirect to Paytrail payment page."""
        transaction = request.env['payment.transaction'].sudo().browse(transaction_id)
        redirect_url = transaction.provider_id.create_paytrail_payment(transaction)
        _logger.info("Redirecting user to Paytrail payment page: %s", redirect_url)
        return redirect(redirect_url, code=302)

    @http.route('/payment/paytrail/success', type='http', auth='public', website=True)
    def paytrail_success(self, **kwargs):
        """Payment successful return from Paytrail."""
        reference = kwargs.get('checkout-reference')
        transaction = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)

        if transaction:
            transaction.provider_reference = kwargs.get('checkout-transaction-id')
            transaction._set_done()
            _logger.info("Transaction %s marked as done", reference)

        return request.redirect('/payment/status')

    @http.route('/payment/paytrail/cancel', type='http', auth='public', website=True)
    def paytrail_cancel(self, **kwargs):
        """Payment canceled return from Paytrail."""
        reference = kwargs.get('checkout-reference')
        transaction = request.env['payment.transaction'].sudo().search([('reference', '=', reference)], limit=1)

        if transaction:
            transaction.provider_reference = kwargs.get('checkout-transaction-id')
            transaction._set_canceled()
            _logger.info("Transaction %s canceled by user", reference)

        return request.redirect('/payment/status?cancel=true')