import os
import gspread
import requests
from flask import Flask, request
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import pandas as pd
import json
from bs4 import BeautifulSoup

