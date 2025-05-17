from rest_framework import serializers
from .models import Topic, Subtopic, Post, Comment




class TopicSerializer(serializers.ModelSerializer):
   subtopics = serializers.SerializerMethodField()
   post = serializers.SerializerMethodField()
   created_by = serializers.ReadOnlyField(source='created_by.username')

   class Meta:
        model = Topic
        fields = ['id', 'title', 'description','subtopics']



class SubtopicSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    child_subtopics = serializers.SerializerMethodField()

    class Meta:
        model = Subtopic
        fields = ['id', 'title', 'description', 'parent_subtopic','child_subtopics']

    def get_child_subtopics(self,obj):
        children = Subtopic.objects.filter(parent_subtopic=obj.id)
        return SubtopicSerializer(children, many=True, context=self.context).data
    
    def validate(self, data):
        if 'parent_topic' not in data and 'parent_subtopic' not in data:
            raise serializers.ValidationError("Subtopic must belong to a Topic, or Subtopic.")
        
        if 'parent_subtopic' in data and 'parent_topic' in data:
            raise serializers.ValidationError("Subtopic cannot belong to both a Topic and Subtopic.")
        
        return data