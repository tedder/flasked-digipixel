import flask
from flask import request,Response
from PIL import Image
from StringIO import StringIO
 
app = flask.Flask(__name__)

#Set app.debug=true to enable tracebacks on Beanstalk log output. 
#Make sure to remove this line before deploying to production.
app.debug=True
 
@app.route('/')
def hello_world():
	app.logger.debug("foolio")
	return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action="/upload" method=post enctype=multipart/form-data>
<!--
<input type="text" name="ff" value="xx">
-->
<p><input type=file name=file>
<input type=submit value=Upload>
</form>
	'''

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	app.logger.debug("hi. method=%s" % request.method)
	if request.method == 'POST':
		app.logger.debug("yup!, method=%s" % request.method)
		f = request.files['file']
		img = Image.open( StringIO(f.read()) )
		# useful:
		# img.split() http://pillow.readthedocs.org/en/latest/reference/Image.html#PIL.Image.Image.split
		# 
		#for x in xrange(0, img.size[1]):
		max_y = 32
		if img.size[0] < 32:
			max_y = img.size[0]
		ss = ""
		ss = ss + "max y: %s\n" % max_y
		ss = ss + "formatter: {0:#0%ib}\n" % max_y
		for x in xrange(0, img.size[1]):
			red = 0
			for y in xrange(0, max_y):
				pixel = img.getpixel( (x,y) )
				#ss = ss + "looking: %s %s // %s\n" % (x, y, pixel[0])
				if pixel[0] > 127:
					#ss = ss + "yay space %s %s / %s\n" % (x, y, pixel[0])
					red = red + (1 << (max_y - y))
					#ss = ss + "red: %s\n" % red
				#ss = ss + "%s %s<br />\n" % (str(img.getpixel( (x,y) )), bin(red))
				#ss = ss + "%s<br />\n" % (bin(red))
			# +2 on y because "0b" counts as two characters.
			ss = ss + ("{0:#0%ib}\n" % (max_y + 2) ).format(red)
			#ss = ss + "(done with row, red = %s)<br />\n" % red

		return "<pre>%s</pre>" % ss
	return "NOPE, method=%s" % request.method
 
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)

