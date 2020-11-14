from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
import math

from django.shortcuts import render

from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions

def MaHoa(plaintext, key):
    ciphertext=""
    for c in plaintext:
        if c!=' ':
            so = ord(c) - 65;
            so = (so + key) % 26
            ciphertext = ciphertext+ chr(so+ 65)
        else:
            ciphertext=ciphertext+c
    return ciphertext

def GiaiMa (ciphertext, key):
    plaintext = ""
    for c in ciphertext:
        if c != ' ':
            so = ord(c)- 65
            so = (so -key + 26) % 26
            plaintext = plaintext+ chr(so+ 65)
        else:
            plaintext = plaintext+c
    return plaintext

def prime_check(a):
    if(a==2):
        return True
    elif((a<2) or ((a%2)==0)):
        return False
    elif(a>2):
        for i in range(2,a):
            if not(a%i):
                return False
    return True

def egcd(e, r):
    while (r != 0):
        e, r = r, e % r
    return e

# Euclid's Algorithm
def eugcd(e, r):
    for i in range(1, r):
        while (e != 0):
            a, b = r // e, r % e
            if (b != 0):
                print("%d = %d*(%d) + %d" % (r, a, e, b))
            r = e
            e = b

# Extended Euclidean Algorithm
def eea(a, b):
    if (a % b == 0):
        return (b, 0, 1)
    else:
        gcd, s, t = eea(b, a % b)
        s = s - ((a // b) * t)
        print("%d = %d*(%d) + (%d)*(%d)" % (gcd, a, t, s, b))
        return (gcd, t, s)

# Multiplicative Inverse
def mult_inv(e, r):
    gcd, s, _ = eea(e, r)
    if (gcd != 1):
        return None
    else:
        if (s < 0):
            print("s=%d. Since %d is less than 0, s = s(modr), i.e., s=%d." % (
            s, s, s % r))
        elif (s > 0):
            print("s=%d." % (s))
        return s % r

def encrypt(pub_key,n_text):
    e,n=pub_key
    x=[]
    m=0
    for i in n_text:
        if(i.isupper()):
            m = ord(i)-65
            c=(m**e)%n
            x.append(c)
        elif(i.islower()):
            m= ord(i)-97
            c=(m**e)%n
            x.append(c)
        elif(i.isspace()):
            spc=400
            x.append(400)
    return x

#Decryption
'''DECRYPTION ALGORITHM'''
def decrypt(d, n, c_text):
    txt = c_text.split(',')
    print(txt)
    x = ''
    m = 0
    for i in txt:
        if (i == '400'):
            x += ' '
        else:
            m = (int(i) ** d) % n
            m += 65
            c = chr(m)
            x += c
    return x


# Create your views here.
class TestApiView(APIView):
    """Test API View"""
    serializer_class = serializers.TestSerializer

    def get(self, request, format=None):
        ret_json = {
            "Message": "Test get api view django",
            "Status": 200
        }

        return Response({
            "Message": "Hello user!",
            "ret_json": ret_json
        })

    def post(self, request):
        """get posted data and say hello"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({
                'Message': message
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )


class MaHoaVanBan(APIView):
    serializer_class = serializers.MaHoa

    def get(self, request, format=None):
        ret_json = {
            "Message": "Nhập văn bản và key để mã hóa dữ liệu",
            "Status": 200
        }
        return Response(
            {
                "Message": ret_json
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            plaintext = serializer.validated_data.get('văn_Bản')
            p = plaintext.upper()
            key = serializer.validated_data.get('key')
            c = MaHoa(p, key)

            return Response(
                {
                    "Văn bản bạn đã nhập": plaintext,
                    "Key bạn đã nhập": key,
                    "Kết quả sau khi mã hóa": c
                }
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class GiaiMaVanBan(APIView):
    serializer_class = serializers.GiaiMa

    def get(self, format=None):
        ret_json = {
            "Message": "Nhập văn bản kèm theo key để giải mã",
            "Status": 200
        }
        return Response(
            {
                "Message": ret_json
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ciphertext = serializer.validated_data.get('văn_Bản')
            c = ciphertext.upper()
            key = serializer.validated_data.get('key')
            plainttext = GiaiMa(c, key)
            return Response(
                {
                    "Văn bản sau khi giải mã": plainttext
                }
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class MaHoaRSA(APIView):
    serializer_class = serializers.MaHoaRSA

    def get(self, format=None):
        ret_json = {
            "Message": "Đặt giá trị cho p và q với điều kiện",
            "Điều kiện": "p và q phải là 2 số nguyên tố"
        }
        return Response(
            {
                "Message": ret_json
            }
        )

    def post (self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            plaintext = serializer.validated_data.get('văn_Bản')
            p = serializer.validated_data.get('p_value')
            q = serializer.validated_data.get('q_value')
            check_p = prime_check(p)
            check_q = prime_check(q)
            if check_p==False or check_q==False:
                return Response(
                    {
                        "Message": 'Yêu cầu nhập giá trị p và q hợp lệ'
                    }
                )
            n = p*q
            r = (p-1)*(q-1)
            for i in range(1, 1000):
                if (egcd(i, r) == 1):
                    e = i
            d = mult_inv(e, r)
            public = (e, n)
            private = (d, n)
            enc_message = encrypt(public, plaintext)
            return Response(
                {
                    "RSA Modulus(N) là": n,
                    "Eulers Toitent(n) là:": r,
                    "Giá trị của e là": e,
                    "Giá trị của d là": d,
                    "Public Key là": f' {public} ',
                    "Private Key là": f' {private} ',
                    "Văn bản sau khi mã hóa RSA": f'{enc_message}'
                }
            )


class GiaiMaRSA(APIView):
    serializer_class = serializers.GiaiMaRSA
    def get(self, format=None):
        ret_json = {
            "Message": "Nhập D và N là hai giá trị của private key để giải mã",
            "Status": 200
        }
        return Response(
            {
                "Message": ret_json
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            plaintext = serializer.validated_data.get('văn_Bản')
            d = serializer.validated_data.get('d')
            n = serializer.validated_data.get('n')
            dec_text = decrypt(d, n, plaintext)
            return Response(
                {
                    f"Văn bản sau khi giải mã sử dụng private key {d, n}": dec_text
                }
            )


class TestViewSet(viewsets.ViewSet):
    """Test API ViewSets"""
    serializer_class = serializers.TestSerializer

    def list(self, request):
        ret_json = {
            'Use actions (list, create, retrieve, update, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provide more functionality with less code'
        }
        return Response({
            'Message': ret_json
        })

    def create(self, request):
        # Create new Hello Message
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({
                'Message': message
            })
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileViewSet(viewsets.ModelViewSet):
    # Handle creating and updating profiles
    """Provide query set to model ViewSet, so we know which objects
    are going to be managed throug this ViewSet"""
    serializer_class = serializers.UserProfileSerial
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email')


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authenication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    """add renderer_classes for default ObtainAuthToken class"""


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    '''Handle creating, reading, and updating profile feed items'''
    # Use Token authentication to authenticate request to our endpoint
    authentication_classes = (TokenAuthentication,)
    # Set serializer class
    serializer_class = serializers.UserProfileFeedSerial
    # Set query
    queryset = models.ProfileFeedItem.objects.all()

    # Create perform_create function
    def perfom_create(self, serializer):
        # Set the user profile to the logged in user
        '''The perform_create function is a handy feature of Django
        rest_framework that allow you to override the behavior or customize the
        behavior for creating objects through a model ViewSet so when a request
        gets made to ViewSet, it get passed into serialized class and validated
        and then these these serialized dots save function is called by default
        If we need to customize the logic for creating an object then we can do
        this by creating the perform_create funtion this perform_create funtion
        get called everytime you do http POST to ViewSet'''
        # Set user profile, save content of serializer to an object in Database
        serializer.save(user_profile=self.request.user)
        '''The request object get passed into all ViewSet every time a request
        is made, it contain all of the details about the request being made to
        the ViewSet because we have added authentication_classes = token
        authenication If user authenticated then the request will have a user
        associated to the authenticated user, if user not authenticated then
        it's just said to an anonymous user account'''
