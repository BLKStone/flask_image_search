# -*- coding:utf-8 -*-
import os
import sys
 
from flask import Flask, render_template, request, jsonify
 
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher

# create flask instance
app = Flask(__name__)

INDEX = os.path.join(os.path.dirname(__file__), 'index.csv')


# main route
@app.route('/')
def index():
    return render_template('index.html')

# search route
@app.route('/search', methods=['POST'])
def search():
 
    if request.method == "POST":
 
        RESULTS_ARRAY = []
 
        # get url
        image_url = request.form.get('img')
        

        try:
 
            # initialize the image descriptor
            cd = ColorDescriptor((8, 12, 3))
 
            # load the query image and describe it
            from skimage import io
            import cv2
            # query = io.imread(image_url)
            # query = (query * 255).astype("uint8")
            # (r, g, b) = cv2.split(query)
            # query = cv2.merge([b, g, r])

            image_url = "app/" + image_url[1:]
            # print "图像url路径:", image_url
            # print os.getcwd()
            # print sys.path[0]
            query = cv2.imread(image_url)
            # print "读取成功！"
            features = cd.describe(query)
            # print "描述子生成成功"
 
            # perform the search
            searcher = Searcher(INDEX)
            results = searcher.search(features)
 
            # loop over the results, displaying the score and image name
            for (score, resultID) in results:
                RESULTS_ARRAY.append(
                    {"image": str(resultID), "score": str(score)})
 
            # return success
            return jsonify(results=(RESULTS_ARRAY[:5]))
 
        except:
 
            # return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500


# run!
if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
