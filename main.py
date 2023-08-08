from fastapi import FastAPI

app = FastAPI()
#change the name app
app.title = "My first app in FastAPI"
#change version
app.version = "0.0.1"
#tags for group routes
@app.get('/',tags=['Home'])
def message():
    return "Hello world"
     