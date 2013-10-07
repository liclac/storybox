from flask.ext.assets import Environment, Bundle

assets = Environment()

bootstrap_js = Bundle('lib/bootstrap/dist/js/bootstrap.js')

css = Bundle(
	'css/style.less',
	
	filters='less', output='gen/style.css'
)

js = Bundle(
	'lib/jquery.js',
	'lib/jquery-autosize/jquery.autosize.js',
	'lib/jquery-selection/src/jquery.selection.js',
	bootstrap_js,
	'js/script.js',
	
	filters=None, output='gen/script.js'
)

assets.register('css_all', css)
assets.register('js_all', js)
