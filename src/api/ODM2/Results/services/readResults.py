import sys
import os
import pandas as pd

from ... import serviceBase
from ..model import *

__author__ = 'Jacob'

class readResults(serviceBase):
    """queries to tables contained in Results schema"""

    """
    TimeSeriesResults
    """
    def getTimeSeriesResults(self):
        """Select all on TimeSeriesResults

        :return TimeSeriesResults Objects:
            :type list:
        """
        return self._session.query(Timeseriesresult).all()

    def getTimeSeriesResultByResultId(self, resultId):
        """Select by resultID on ResultID

        :param resultId:
            :type Integer:
        :return return matching Timeseriesresult Object filtered by resultId
        """

        try:
            return self._session.query(Timeseriesresult).filter_by(ResultID=resultId).one()
        except:
            return None



    """
    TimeSeriesResultValues
    """
    def getTimeSeriesResultValues(self):
        """Select all on TimeSeriesResults

        :return TimeSeriesResultsValue Objects:
            :type list:
        """
        try:
            q=self._session.query(Timeseriesresultvalue).order_by(Timeseriesresultvalue.ValueDateTime).all()
            df = pd.DataFrame([dv.list_repr() for dv in q])
            df.columns = q[0].get_columns()

            return df
        except:
            return None

    def getTimeSeriesResultValuesByResultId(self, resultId):
        """Select by resultId

        :param timeSeriesId:
            :type Integer:
        :return return matching Timeseriesresultvalue Object filtered by resultId:
            :type Timeseriesresultvalue:
        """
        try:
            q=self._session.query(Timeseriesresultvalue).filter_by(ResultID=resultId)\
                .order_by(Timeseriesresultvalue.ValueDateTime).all()


            df = pd.DataFrame([dv.list_repr() for dv in q])
            df.columns = q[0].get_columns()
            return df
            #return self._session.query(Timeseriesresultvalue).filter_by(ResultID=resultId).all()
        except Exception as e:
            return None


    def getTimeSeriesResultValuesByTime(self, resultid, starttime, endtime=None):

        # set end = start if it is None
        endtime = starttime if not endtime else endtime

        try:
            q= self._session.query(Timeseriesresultvalue).filter_by(ResultID=resultid) \
                                                      .filter(Timeseriesresultvalue.ValueDateTime >= starttime) \
                                                      .filter(Timeseriesresultvalue.ValueDateTime <= endtime) \
                                                      .order_by(Timeseriesresultvalue.ValueDateTime).all()




            df = pd.DataFrame([dv.list_repr() for dv in q])
            df.columns = q[0].get_columns()
            return df.sort('ValueDateTime', ascending = True)
        except:
            return None