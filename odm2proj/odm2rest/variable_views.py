
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from collections import OrderedDict

import csv
import pyaml

from odm2service import Service
from negotiation import IgnoreClientContentNegotiation
from dict2xml import dict2xml as xmlify

class VariableViewSet(APIView):
    """
    All ODM2 variables Retrieval
    """
    content_negotiation_class = IgnoreClientContentNegotiation
    #renderer_classes = (JSONRenderer, YAMLRenderer)
    #serializer_class = VariableSerializer

    def get(self, request, format=None):
        """
        ---
        parameters:
            - name: format    
              description: The format type is "yaml", "json", "xml" or "csv". The default type is "json".
              required: false
              type: string
              paramType: query

        omit_serializer: true

        responseMessages:
            - code: 401
              message: Not authenticated
        """

        #accept = request.accepted_renderer.media_type
        mr = MultipleRepresentations()
        format = request.query_params.get('format', mr.default_format)
        readConn = mr.readService()
        items = readConn.getVariables()
        if items == None or len(items) == 0:
            return Response('The data is not existed.',
                            status=status.HTTP_400_BAD_REQUEST)

        return mr.content_format(items, format)

class VariableCodeViewSet(APIView):
    """
    All ODM2 variables Retrieval
    """
    content_negotiation_class = IgnoreClientContentNegotiation

    def get(self, request, format=None, variableCode=None):
        """
        ---
        parameters:
            - name: format    
              description: The format type is "yaml", "json", "xml" or "csv". The default type is "json".
              required: false
              type: string
              paramType: query

        omit_serializer: true

        responseMessages:
            - code: 401
              message: Not authenticated
        """

        if variableCode is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        #accept = request.accepted_renderer.media_type
        mr = MultipleRepresentations()
        format = request.query_params.get('format', mr.default_format)
        readConn = mr.readService()
        items = readConn.getVariableByCode(variableCode)

        if items == None:
            return Response('"%s" is not existed.' % variableCode,
                            status=status.HTTP_400_BAD_REQUEST)

        return mr.content_format(items, format)

class VariableNameViewSet(APIView):
    """
    All ODM2 variables Retrieval
    """
    content_negotiation_class = IgnoreClientContentNegotiation

    def get(self, request, format=None, variableName=None):
        """
        ---
        parameters:
            - name: format    
              description: The format type is "yaml", "json", "xml" or "csv". The default type is "json".
              required: false
              type: string
              paramType: query

        omit_serializer: true

        responseMessages:
            - code: 401
              message: Not authenticated
        """

        if variableName is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        #accept = request.accepted_renderer.media_type
        mr = MultipleRepresentations()
        format = request.query_params.get('format', mr.default_format)
        readConn = mr.readService()
        items = readConn.getVariableByName(variableName)

        if items == None:
            return Response('"%s" is not existed.' % variableName,
                            status=status.HTTP_400_BAD_REQUEST)

        return mr.content_format(items, format)

class VariableTypeViewSet(APIView):
    """
    All ODM2 variables Retrieval
    """
    content_negotiation_class = IgnoreClientContentNegotiation

    def get(self, request, format=None, variableType=None):
        """
        ---
        parameters:
            - name: format    
              description: The format type is "yaml", "json", "xml" or "csv". The default type is "json".
              required: false
              type: string
              paramType: query

        omit_serializer: true

        responseMessages:
            - code: 401
              message: Not authenticated
        """

        if variableType is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        #accept = request.accepted_renderer.media_type
        mr = MultipleRepresentations()
        format = request.query_params.get('format', mr.default_format)
        readConn = mr.readService()
        items = readConn.getVariableByType(variableType)

        if items == None:
            return Response('"%s" is not existed.' % variableType,
                            status=status.HTTP_400_BAD_REQUEST)

        return mr.content_format(items, format)

class MultipleRepresentations(Service):

    def json_format(self):

        return self.sqlalchemy_object_to_dict()

    def csv_format(self):

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="variables.csv"'

        variable_csv_header = ["#fields=VariableTypeCV[type='string']","VariableCode[type='string']","VariableNameCV[type='string']","VariableDefinition[type='string']","SpeciationCV[type='string']","NoDataValue"]

        writer = csv.writer(response)
        writer.writerow(variable_csv_header)
            
        for variable in self.items:
            row = []
            row.append(variable.VariableTypeCV)
            row.append(variable.VariableCode)
            row.append(variable.VariableNameCV)
            row.append(variable.VariableDefinition)
            row.append(variable.SpeciationCV)
            row.append(variable.NoDataValue)

            writer.writerow(row)

        self._session.close()
        return response

    def yaml_format(self):

        response = HttpResponse(content_type='application/yaml')
        response['Content-Disposition'] = 'attachment; filename="variables.yaml"'

        response.write("---\n")
        allvars = {}
        vararray = self.sqlalchemy_object_to_dict()
        allvars["Variables"] = vararray
        response.write(pyaml.dump(allvars,vspacing=[0, 0]))
        return response

    def xml_format(self):
        response = HttpResponse(content_type='text/xml')
        response['Content-Disposition'] = 'attachment; filename="variables.xml"'

        response.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")

        allvars = self.sqlalchemy_object_to_dict()
        response.write(xmlify({'Variable': allvars}, wrap="Variables", indent="  "))
        return response

    def sqlalchemy_object_to_dict(self):

        allvars = []
        for variable in self.items:
            queryset = OrderedDict()
            #queryset['VariableID'] = variable.VariableID
            queryset['VariableCode'] = variable.VariableCode
            queryset['VariableType'] = variable.VariableTypeCV
            queryset['VariableName'] = variable.VariableNameCV
            queryset['VariableDefinition'] = variable.VariableDefinition
            queryset['NoDataValue'] = variable.NoDataValue
            queryset['Speciation'] = variable.SpeciationCV
            allvars.append(queryset)

        self._session.close()
        return allvars

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

