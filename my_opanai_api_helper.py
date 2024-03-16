import openai

openai.api_key = "YOUR_API_KEY_HERE"
COMPLETION_MODEL_NAME = "gpt-3.5-turbo-instruct"
MAX_LISTINGS_TO_GENERATE = 20
MAX_ANSWER_TOKENS = 3000

#This method handles a call to the OpenAI completion model
def callOpenAi(prompt):
    try:
        response = openai.Completion.create(
            model=COMPLETION_MODEL_NAME,
            prompt=prompt,
            max_tokens=MAX_ANSWER_TOKENS
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        print(e)
        return ""

#Call open AI to generate listings. This has been run to generate the original listings that are now stored in Listings.txt
def generate_listings(num_listings):
    prompt = create_generate_listings_prompt(num_listings)
    return callOpenAi(prompt)

#Usee LLM to augment a listing
#num_words - is the max number of words in the augmented description
#preferences_list - The user preferences. We will augment the listing based on these preferences
#original_description - The original listing description
def augment_listing(num_words, preferences_list, original_description):
    prompt = create_augment_listing_prompt(num_words, preferences_list, original_description)
    return callOpenAi(prompt)

#Crate the LLM prompt that will generate the listings
def create_generate_listings_prompt(num_listings):


    num_listings = MAX_LISTINGS_TO_GENERATE if num_listings > MAX_LISTINGS_TO_GENERATE else num_listings
    json_example = """
        {
                "listings": [
                    {
                        "id": 1,
                        "neighborhood": "Green Oaks",
                        "price": 800000,
                        "bedrooms": 2,
                        "bathrooms": 2,
                        "size_sqft": 2000,
                        "description": "Welcome to this eco-friendly oasis nestled in the heart of Green Oaks. This charming 3-bedroom, 2-bathroom home boasts energy-efficient features such as solar panels and a well-insulated structure. Natural light floods the living spaces, highlighting the beautiful hardwood floors and eco-conscious finishes. The open-concept kitchen and dining area lead to a spacious backyard with a vegetable garden, perfect for the eco-conscious family. Embrace sustainable living without compromising on style in this Green Oaks gem.",
                        "neighborhood description": "Green Oaks is a close-knit, environmentally-conscious community with access to organic grocery stores, community gardens, and bike paths. Take a stroll through the nearby Green Oaks Park or grab a cup of coffee at the cozy Green Bean Cafe. With easy access to public transportation and bike lanes, commuting is a breeze."
                    },
                    {
                        "id": 2,
                        "neighborhood": "Green Oaks",
                        "price": 1000000,
                        "bedrooms": 4,
                        "bathrooms": 2,
                        "size_sqft": 4000,
                        "description": "Welcome to....",
                        "neighborhood description": "Green Oaks is a...."
                    }
                ]
            }
    """
    return f"""

            Generate {num_listings} real estate listings with the format below:

            
            {json_example}
            
            The "id" is an increasing number starting at 1
            Make sure "description" Is a text of up to 75 words
            Make sure "neighborhood description" Is a text of up to 50 words

        """

#Crate the LLM prompt that will augment a listing based on user preferences
def create_augment_listing_prompt(num_words, preferences_list, original_description):

    task = f"""Rewrite the description of the real estate listing below in {num_words} words,
    emphasizing on things that are important to the buyer while maintaining the factual integrity of the listing description
    """
    
    preferences = "\n".join(preferences_list)

    return f"""
        {task}

        Description: "{original_description}"

        Customer preferences: "
            {preferences}
        "
    """