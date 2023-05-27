# portugal_trip/views.py

from django.http import HttpResponse

def index(request):
    blog = """ My first Europe trip was to Portugal.</br>
    <br>It was an amazing experience for the following reasons:</br>
    <br>1. Architecture - The cobble stone roads, bridges, buildings, cathedrals,
    <br>                  and castles dated back several years was a site to see.
    <br>                  I recommend touring the Pena Palace in Sintra.</br>
    <br>2. Cuisine - The food was delicious (especially if you like seafood).
    <br>             I tried octopus, various fish, meats, wine, coffee and cheeses.
    <br>             I recommend any cheeses, and "bacalhau" (cod fish).</br>
    <br>3. Night Life - The night life was live: music, food, and drinks all available
    <br>                on the streets of Lisbon and Algarve. Lots of tourists here.</br>
    <br>4. Beaches - The beaches displayed beautiful scenery, clear blue waters and soft sand.
    <br>             The main beaches are in Algarve, and there are many to choose from.</br>
    <br>5. Mountains - Lastly, there are so many mountains that provide breath taking views,
    <br>               and even fresh water streams. I recommend touring Serra da Estrela,
    <br>               one of the highest mountain ranges in Portugal.</br>
    <br>There are so many places in Portugal I have yet to discover.
    <br>Nonetheless, I highly recommend adding Portugal to your travel bucket list!</br>
    <br>-Brandon Orellana
    """
    return HttpResponse(blog)