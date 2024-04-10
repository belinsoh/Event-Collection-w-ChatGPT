import os
from openai import OpenAI
import pandas as pd
import json

client = OpenAI(
    api_key= "insert API key here"
)

function_global_disaster = [
{
    "name": "presentGlobalDisasters",
    "description": "Presents the Global disasters to the user.",
    "parameters": 
    {
        "type": "object",
        "properties": 
        {
            "disasters": 
            {
                "type": "array",
                "description": "disaster name with duplicate entries if happen on multiple days",
                "items": {
                    "type": "object",
                    "properties": {
                        "Name": 
                        {
                            "type": "string",
                            "description": "name of disaster event"
                        },
                        "date": 
                        {
                            "type": "string",
                            "description":"date of disaster when is still occurring in format of dd-mm-yy"
                        },
                        "impact on demand": 
                        {
                            "type": "integer",
                            "description": "global disaster's impact on Singapore's demand of beverages on scale of -5 to 5, where 0 is no impact, -5 is large negative impact and 5 is large positive impact."
                        }
                    }
                }
            }
        }
    }
}]

global_disaster_df = {}
for year in range (2017, 2019):
    year = str(year)
    response = client.chat.completions.create(
            messages=[
                { "role": "system", "content": "You are a friendly assistant and you will always call the provided functions." },
                { "role": "user", "content": "Combine a list and description of all disasters, manmade or natural, that had global impact in" + year +". Repeat entry for each date disaster falls on if it is over a period of multiple dates" }
            ],
            functions = function_global_disaster,
            function_call = {"name": "presentGlobalDisasters"},
            model="gpt-4-turbo-preview",
        )
    
    argument = response.choices[0].message.function_call.arguments
    json_obj = json.loads(argument)
    df = pd.json_normalize(json_obj["disasters"])
    global_disaster_df[year] = df

function_asia_disaster = [
{
    "name": "presentAsiaDisasters",
    "description": "Presents the asia disasters to the user.",
    "parameters": 
    {
        "type": "object",
        "properties": 
        {
            "disasters": 
            {
                "type": "array",
                "description": "disaster name with duplicate entries if happen on multiple days",
                "items": {
                    "type": "object",
                    "properties": {
                        "Name": 
                        {
                            "type": "string",
                            "description": "name of disaster event"
                        },
                        "date": 
                        {
                            "type": "string",
                            "description":"date of disaster when is still occurring in format of dd-mm-yy"
                        },
                        "impact on demand": 
                        {
                            "type": "integer",
                            "description": "regional disaster's impact on Singapore's demand of beverages on scale of -5 to 5, where 0 is no impact, -5 is large negative impact and 5 is large positive impact."
                        }
                    }
                }
            }
        }
    }
}]

asia_disaster_df = {}
for year in range (2017, 2019):
    year = str(year)
    response = client.chat.completions.create(
            messages=[
                { "role": "system", "content": "You are a friendly assistant and you will always call the provided functions." },
                { "role": "user", "content": "Combine a list and description of all disasters, manmade or natural, that happened in Asia, excluding Singapore's, in" + year +". Repeat entry for each date disaster falls on if it is over a period of multiple dates" }
            ],
            functions = function_asia_disaster,
            function_call = {"name": "presentAsiaDisasters"},
            model="gpt-4-turbo-preview",
        )
    
    argument = response.choices[0].message.function_call.arguments
    json_obj = json.loads(argument)
    df = pd.json_normalize(json_obj["disasters"])
    asia_disaster_df[year] = df

function_local_disaster = [
{
    "name": "presentLocalDisasters",
    "description": "Presents the disasters to the user.",
    "parameters": 
    {
        "type": "object",
        "properties": 
        {
            "disasters": 
            {
                "type": "array",
                "description": "disaster name with duplicate entries if happen on multiple days",
                "items": {
                    "type": "object",
                    "properties": {
                        "Name": 
                        {
                            "type": "string",
                            "description": "name of disaster event"
                        },
                        "date": 
                        {
                            "type": "string",
                            "description":"date of disaster when is still occurring in format of dd-mm-yy"
                        },
                        "impact on demand": 
                        {
                            "type": "integer",
                            "description": "disaster's impact on Singapore's demand of beverages on scale of -5 to 5, where 0 is no impact, -5 is large negative impact and 5 is large positive impact."
                        }
                    }
                }
            }
        }
    }
}]

local_disaster_df = {}
for year in range (2017, 2019):
    year = str(year)
    response = client.chat.completions.create(
            messages=[
                { "role": "system", "content": "You are a friendly assistant and you will always call the provided functions." },
                { "role": "user", "content": "Combine a list and description of all disasters, manmade or natural, that happened in Singapore in" + year +". Repeat entry for each date disaster falls on if it is over a period of multiple dates" }
            ],
            functions = function_local_disaster,
            function_call = {"name": "presentLocalDisasters"},
            model="gpt-4-turbo-preview",
        )
    
    argument = response.choices[0].message.function_call.arguments
    json_obj = json.loads(argument)
    df = pd.json_normalize(json_obj["disasters"])
    local_disaster_df[year] = df

frames = [local_disaster_df.get("2017"), asia_disaster_df.get("2017"), global_disaster_df.get("2017"), local_disaster_df.get("2018"), asia_disaster_df.get("2018"), global_disaster_df.get("2018")]
result = pd.concat(frames)
result.to_csv("DisasterEvents.csv", encoding='utf-8', index=False)
