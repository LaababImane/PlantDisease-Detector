from fastapi import FastAPI, Request, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from tensorflow.python.keras.backend import argmax
import uvicorn
import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf

app = FastAPI()
templates = Jinja2Templates(directory="/src/templates")

origins = [
    "http://localhost",
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:5000",
    "http://127.0.0.1:8000/predictPotato"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_POTATO = tf.keras.models.load_model("Models/Potato.h5")
POTATO_CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]
POTATO_CAUSE = ["Fungus [Alternaria solani]",
                "Water Mold [Phytophthora infestans]", 
                "None"]
POTATO_DISC = ["Affects leaves, stems and tubers and can reduce yield, tuber size, storability of tubers, quality of fresh-market and processing tubers and marketability of the crop",
               "Infect potato foliage and tubers at any stage of crop development", 
               "None"]
POTATO_TREAT = ["Thoroughly spray the plant (bottoms of leaves also) with Bonide Liquid Copper Fungicide concentrate",
                "Fungicides that contain maneb, mancozeb, chlorothanolil, or fixed copper", "None"]
POTATO_PREVENTION = ["Planting potato varieties, Avoid overhead irrigation and allow for sufficient aeration between plants to allow the foliage to dry as quickly as possible",
                "Eliminating cull piles and volunteer potatoes, using proper harvesting and storage practices, and applying fungicides when necessary, Air drainage to facilitate the drying of foliage each day is important", "None"]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image
    


@app.get("/a", response_class=HTMLResponse)
def write_home(request: Request, user_name: str):
    return templates.TemplateResponse("home.html")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predictPotato")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL_POTATO.predict(img_batch)

    predicted_class = POTATO_CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    casue = POTATO_CAUSE[np.argmax(predictions[0])]
    disc = POTATO_DISC[np.argmax(predictions[0])]
    treat = POTATO_TREAT[np.argmax(predictions[0])]
    prevent = POTATO_PREVENTION[np.argmax(predictions[0])]
    
    return {
        'class': predicted_class,
        'confidence': float(confidence),
        'cause': casue,
        'dispcription': disc,
        'treatment': treat,
        'prevention' : prevent,
    }
#this is just a api test
# @app.post("/api/predict")
# async def predict(image: UploadFile):
#     # Use your trained model to predict the disease
#     # Return the disease name and other relevant info
#     return {"disease": "Potato early blight", "confidence": 0.87, "treatment": "Apply copper fungicides."}



APPLE_CLASS_NAMES = ["Apple Scab", "Black Rot", "Cedar Apple Rust", "Healthy"]
MODEL_APPLE = tf.keras.models.load_model("Models/Apple.h5")
APPLE_CAUSE = ["Fungus [Venturia inaequalis]",
               "Fungus [Diplodia seriata]",
               "Pathogen [Gymnosporangium juniperi-virginianae]", 
               "None"]
APPLE_DISC = ["Overwinters on fallen diseased leaves. In spring, these fungi shoot spores into the air. Spores are carried by wind to newly developing leaves, flowers, fruit or green twigs",
              "Overwinters in cankers, mummified fruits, and the bark of dead wood",
              "Reduce yield on apples, blemish the fruit, and lead to weakening and death of redcedar",
               "None"]
APPLE_TREAT = ["Fungicide application must begin in early spring from apple green tip, and continue on a 7- to 10-day schedule (7 days during wet weather, 10 days if dry) until petal fall. If dry weather persists after petal fall, a 10- to 14-day spray schedule is adequate for scab control.",
               "Mancozeb, and Ziram are all highly effective against black rot", 
               "Fungicides with the active ingredient Myclobutanil are most effective in preventing rust, Spray trees and shrubs when flower buds first emerge until spring weather becomes consistently warm and dry, Monitor nearby junipers ",
               "None"]
APPLE_PREVENTION = ["Choose scab-resistant varieties of apple or crabapple trees, Rake up and discard any fallen leaves or fruit on a regular basis, and never leave fallen leaves or fruit on the ground over winter",
               "Prune out dead or diseased branches, Pick all dried and shriveled fruits remaining on the trees, Remove infected plant material from the area, All infected plant parts should be burned, buried or sent to a municipal composting site, Be sure to remove the stumps of any apple trees you cut down", 
               "Control of cedar–apple rust will be best obtained by growing apple varieties that are less susceptible ",
               "None"]

@app.post("/predictApple")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)
    
    predictions = MODEL_APPLE.predict(img_batch)
    
    predicted_class = APPLE_CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    casue = APPLE_CAUSE[np.argmax(predictions[0])]
    disc = APPLE_DISC[np.argmax(predictions[0])]
    treat = APPLE_TREAT[np.argmax(predictions[0])]
    prevent = APPLE_PREVENTION[np.argmax(predictions[0])]
    return {
        'class': predicted_class,
        'confidence': float(confidence),
        'cause': casue,
        'dispcription': disc,
        'treatment': treat,
        'prevention' : prevent
    }


MODEL_STRAWBERRY = tf.keras.models.load_model("Models/Strawberry.h5")
STRAWBERRY_CLASS_NAMES = [ "Leaf Scorch", "Health"]
STRAWBERRY_CAUSE = ["Fungus [Diplocarpon Earlianum]", "None"]
STRAWBERRY_DISC = ["This ascomycete produces disk-shaped, dark brown to black apothecia (0.25-1 mm) on advanced-stage lesions on strawberry leaves and leaf residues (Heidenreich and Turechek).", "None"]
STRAWBERRY_TREAT = ["No Known Cure", "None"]
STRAWBERRY_PREVENTION = ["Prevention of scorch needs to begin with winter watering. A deep soaking once a month, when there is no snow cover, will help prevent root die-back due to dehydration.", "None"]
@app.post("/predictStrawberry")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL_STRAWBERRY.predict(img_batch)

    predicted_class = STRAWBERRY_CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])
    casue = STRAWBERRY_CAUSE[np.argmax(predictions[0])]
    disc = STRAWBERRY_DISC[np.argmax(predictions[0])]
    treat = STRAWBERRY_TREAT[np.argmax(predictions[0])]
    prevent = STRAWBERRY_PREVENTION[np.argmax(predictions[0])]
    return {
        'class': predicted_class,
        'confidence': float(confidence),
        'cause': casue,
        'dispcription': disc,
        'treatment': treat,
        'prevention' : prevent
    }


if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)

