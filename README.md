# Inkscape as a service

A simple web service that transforms the given SVG file into the desired format. 

Run with `docker run -p 8080:8080 gcr.io/as-a-service-dev/inkscape`

### URL parameters:

* `input`: URL of the document to transform.

## Running the server locally

* Build with `docker build . -t pdf`
* Start with `docker run -p 8080:8080 inkscape`
* Open in your browser at `http://localhost:8080"/?url=https://upload.wikimedia.org/wikipedia/commons/f/fd/Ghostscript_Tiger.svg`

## Deploy to your server

The following container image always reflects the latest version of the `master` branch of this repo: `gcr.io/as-a-service-dev/inkscape`

## Deploy to Google Cloud

[![Run on Google Cloud](https://storage.googleapis.com/cloudrun/button.svg)](https://console.cloud.google.com/cloudshell/editor?shellonly=true&cloudshell_image=gcr.io/cloudrun/button&cloudshell_git_repo=https://github.com/as-a-service/pdf.git)

Or use `gcloud beta run deploy --image gcr.io/as-a-service-dev/inkscape`
