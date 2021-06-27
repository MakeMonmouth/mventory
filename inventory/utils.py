from django.conf import settings
from six.moves import urllib
import json
import os

# copy pasted from: https://github.com/prisma-labs/python-graphql-client/blob/master/graphqlclient/client.py
class OctopartClient:
    def __init__(self):
        self.endpoint = getattr(settings, "OCTOPART_API_ENDPOINT", None)
        self.token = getattr(settings, "OCTOPART_API_KEY", None)
        self.headername = 'token'

    def execute(self, query, variables=None):
        return self._send(query, variables)

    def inject_token(self, token, headername='token'):
        self.token = token
        self.headername = headername

    def _send(self, query, variables):
        data = {'query': query,
                'variables': variables}
        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}

        if self.token is not None:
            headers[self.headername] = '{}'.format(self.token)

            req = urllib.request.Request(self.endpoint, json.dumps(data).encode('utf-8'), headers)
            
            try:
                response = urllib.request.urlopen(req)
                return response.read().decode('utf-8')
            except urllib.error.HTTPError as e:
                raise e
        else:
            response= json.dumps({
                "data": {
                    "multi_match": 
                        [
                            {
                            "hits": 0
                            }
                            ]
                    }
                })
            return response

    def get_parts(self, ids):
        query = '''
        query get_parts($ids: [String!]!) {
            parts(ids: $ids) {
                id
                manufacturer {
                    name
                }
                mpn
                category {
                    name
                }
            }
        }
        '''

        ids = [str(id) for id in ids]
        resp = self.execute(query, {'ids': ids})
        return json.loads(resp)['data']['parts']

    def match_mpns(self, mpns):
        dsl = '''
        query match_mpns($queries: [PartMatchQuery!]!) {
            multi_match(queries: $queries) {
                hits
                reference
                parts {
                    document_collections {
                      documents {
                        name
                        url
                      }
                    }
                    manufacturer {
                        name
                    }
                    mpn
                }
            }
        }
        '''

        queries = []
        for mpn in mpns:
            queries.append({
                'mpn_or_sku': mpn,
                'start': 0,
                'limit': 5,
                'reference': mpn,
            })
        resp = self.execute(dsl, {'queries': queries})
        return json.loads(resp)['data']['multi_match']
