import logging
import json
from datetime import datetime

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, post_review
from .utils import get_sentiment
# Module import
from .restapis import get_request, analyze_review_sentiments, post_review, searchcars_request


# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create a `login_request` view to handle sign-in request
@csrf_exempt
def login_user(request):
    """Handle user login."""
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    response_data = {"userName": username}
    if user:
        login(request, user)
        response_data["status"] = "Authenticated"
    return JsonResponse(response_data)

# Create a `logout_request` view to handle sign-out request
def logout_request(request):
    """Handle user logout."""
    logout(request)
    return JsonResponse({"userName": ""})

# Create a `registration` view to handle sign-up request
@csrf_exempt
def registration(request):
    """Handle user registration."""
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    try:
        # Check if user already exists
        User.objects.get(username=username)
        return JsonResponse({"userName": username, "error": "Already Registered"})
    except User.DoesNotExist:
        logger.debug(f"{username} is a new user")

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})

# A method to get the list of cars from the model
def get_cars(request):
    """Get the list of cars."""
    if not CarMake.objects.exists():
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = [
        {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        for car_model in car_models
    ]
    return JsonResponse({"CarModels": cars})

# Update the `get_dealerships` view to render the index page with a list of dealerships by states
def get_dealerships(request, state="ALL"):
    """Get a list of dealerships."""
    endpoint = f"/fetchDealers{f'/{state}' if state != 'ALL' else ''}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# A method to get dealers by ID's
def get_dealer_details(request, dealer_id):
    """Get dealer details by ID."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request. Invalid Dealer ID"})
    endpoint = f"/fetchDealer/{dealer_id}"
    dealership = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer": dealership})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    """Get reviews for a dealer."""
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request. Invalid Dealer ID"})
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)
    for review_detail in reviews:
        sentiment = get_sentiment(review_detail['review'])
        review_detail['sentiment'] = sentiment
    return JsonResponse({"status": 200, "reviews": reviews})

# Create an `add_review` view to submit a review
def add_review(request):
    """Submit a review."""
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized. Please sign in to post a review"})
    data = json.loads(request.body)
    try:
        post_review(data)
        return JsonResponse({"status": 200})
    except Exception as e:
        logger.error(f"Error in posting review: {e}")
        return JsonResponse({"status": 401, "message": "Error posting review. Check your connection or contact support"})



# Code for the view
def get_inventory(request, dealer_id):
    data = request.GET
    if (dealer_id):
        if 'year' in data:
            endpoint = "/carsbyyear/"+str(dealer_id)+"/"+data['year']
        elif 'make' in data:
            endpoint = "/carsbymake/"+str(dealer_id)+"/"+data['make']
        elif 'model' in data:
            endpoint = "/carsbymodel/"+str(dealer_id)+"/"+data['model']
        elif 'mileage' in data:
            endpoint = "/carsbymaxmileage/"+str(dealer_id)+"/"+data['mileage']
        elif 'price' in data:
            endpoint = "/carsbyprice/"+str(dealer_id)+"/"+data['price']
        else:
            endpoint = "/cars/"+str(dealer_id)
 
        cars = searchcars_request(endpoint)
        return JsonResponse({"status": 200, "cars": cars})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})
    return JsonResponse({"status": 400, "message": "Bad Request"})
