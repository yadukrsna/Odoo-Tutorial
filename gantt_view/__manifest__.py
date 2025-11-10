{
    'name': "Gantt View",
    'version': '1.0',
    'depends': ['base', 'web', 'project'],
    'license': 'LGPL-3',
    'data': [
        'views/project_task_view.xml',
    ],
    'assets': {
      'web.assets_backend': [
          'gantt_view/static/src/js/gantt_arch_parser.js',
          'gantt_view/static/src/js/gantt_model.js',
          'gantt_view/static/src/js/gantt_controller.js',
          'gantt_view/static/src/xml/gantt_controller.xml', 
          'gantt_view/static/src/js/gantt_renderer.js',
          'gantt_view/static/src/js/gantt_view.js',
      ],
    },
    'installable': True,
    'application': False,
    'auto_install': True,
}