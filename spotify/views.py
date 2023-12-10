from django.shortcuts import render
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URL
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import requests



