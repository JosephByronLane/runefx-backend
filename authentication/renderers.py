from rest_framework.renderers import JSONRenderer

class TokenRemovingJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict):         
            if 'access' in data:
                del data['access']
            if 'refresh' in data:
                del data['refresh']
                
        return super().render(data, accepted_media_type, renderer_context)