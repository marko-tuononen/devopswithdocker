import io
import os
import tempfile
import shutil

import pytest

import app as myapp

def assert_not_found(response):
    assert response.status_code == 404
    assert b'404 Not Found' in response.data

def assert_missing_image(response):
    assert response.status_code == 400
    assert b'missing image' in response.data

def assert_files_in_upload_folder(expected_num_files): 
    assert os.path.exists(myapp.app.config["UPLOAD_FOLDER"])
    assert len(os.listdir(myapp.app.config["UPLOAD_FOLDER"])) == expected_num_files

def do_persist_image(client,image_data,image_name,label):
    data = { "image": (io.BytesIO(image_data), image_name) }
    return client.post(
        "/persist/"+label,
        data=data, 
        follow_redirects=True,
        content_type='multipart/form-data'
    )

def persist_image(client,image_file,label):
        image_data = image_file.read()
        image_name = os.path.basename(image_file.name)
        response = do_persist_image(client, image_data, image_name, label)
        assert response.status_code == 200
        assert b'"label":"'+label.encode('ascii')+b'"' in response.data
        path = myapp.app.config["UPLOAD_FOLDER"] + "/" + label
        assert os.path.exists(path)
        assert len(os.listdir(path)) == 1

def do_predict_image(client,image_data,image_name):
    data = { "image": (io.BytesIO(image_data), image_name) }
    return client.post(
        "/predict",
        data=data, 
        follow_redirects=True,
        content_type='multipart/form-data'
    )

def predict_image(client,image_file,label):
        image_data = image_file.read()
        image_name = os.path.basename(image_file.name)
        response = do_predict_image(client, image_data, image_name)
        assert response.status_code == 200
        assert b'"label":"'+label.encode('ascii')+b'"' in response.data

@pytest.fixture
def client():
    temp_dir = tempfile.mkdtemp()
    myapp.app.config["UPLOAD_FOLDER"] = temp_dir
    myapp.app.config["TESTING"] = True
    myapp.load_model()
    
    yield myapp.app.test_client()

    shutil.rmtree(temp_dir)

## GENERAL TESTS

def test_empty(client):
    assert_files_in_upload_folder(0)

## TEST ENDPOINT PERSIST

def test_persist_wrong_method(client):
    assert client.get("/persist/horse").status_code == 405
    assert client.head("/persist/horse").status_code == 405
    assert client.put("/persist/horse").status_code == 405
    assert client.delete("/persist/horse").status_code == 405
    assert client.patch("/persist/horse").status_code == 405
    assert client.trace("/persist/horse").status_code == 405

def test_persist_wrong_url(client):
    assert_not_found(client.post("/persist/"))
    assert_not_found(client.post("/persist/horse/cat"))
    assert_not_found(client.post("/persist/../../../cat")) # potentially unsecure

def test_persist_wrong_image(client):
    assert_missing_image(client.post("/persist/horse")) # no image
    assert_missing_image(do_persist_image(client,b"abcdef","test.jpg","horse")) # not recognized as image

def test_persist_image(client):
    with open("tabby_cat.jpg", mode="rb") as file:
        persist_image(client,file,"cat")

    assert_files_in_upload_folder(1)

def test_persist_images(client):
    with open("digit.png", mode="rb") as file:
        persist_image(client,file,"digit")

    with open("tabby_cat.jpg", mode="rb") as file:
        persist_image(client,file,"cat")
    
    assert_files_in_upload_folder(2)

## TEST ENDPOINT PREDICT

def test_predict_wrong_method(client):
    assert client.get("/predict").status_code == 405
    assert client.head("/predict").status_code == 405
    assert client.put("/predict").status_code == 405
    assert client.delete("/predict").status_code == 405
    assert client.patch("/predict").status_code == 405
    assert client.trace("/predict").status_code == 405

def test_predict_wrong_url(client):
    assert_not_found(client.post("/predict/"))
    assert_not_found(client.post("/predict/1"))

def test_predict_wrong_image(client):
    assert_missing_image(client.post("/predict")) # no image
    assert_missing_image(do_predict_image(client,b"abcdef","test.jpg")) # not recognized as image

def test_predict_image(client):
    with open("tabby_cat.jpg", mode="rb") as file:
        predict_image(client,file,"tiger cat")

    with open("digit.png", mode="rb") as file:
        predict_image(client,file,"digital clock")

    assert_files_in_upload_folder(0)
