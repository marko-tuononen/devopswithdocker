Application providing an API to predict what is the object in the image.
Usage: POST image to port 5000

My submission can be found from https://hub.docker.com/repository/docker/markotuononen/image-prediction-app

# docker pull markotuononen/image-prediction-app
...
# docker run -p 5000:5000 markotuononen/image-prediction-app
Downloading: "https://download.pytorch.org/models/densenet161-8d451a50.pth" to /home/appuser/.cache/torch/checkpoints/densenet161-8d451a50.pth
100.0% * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on

 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 136-132-236
172.17.0.1 - - [30/May/2019 16:46:20] "POST /predict HTTP/1.1" 200 -
