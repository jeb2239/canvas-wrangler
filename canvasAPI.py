import itertools
import requests
import os
"""
Taken from:
https://github.com/hawesie/python-canvas-api/blob/master/src/marking/canvas_api.py
"""

class GroupSetBuilder():
    def __init__(self):
        """Construct a set of groups"""
        self.groups = {}

    def add_group_member(self, user_id, group_id):
        if group_id not in self.groups:
            self.groups[group_id] = [user_id]
        else:
            self.groups[group_id].append(user_id)

default_access_token=os.environ["CANVASPONIES"]


class CanvasAPI():
    """"""

    def __init__(self, access_token=default_access_token, base_url='https://courseworks2.columbia.edu', api_prefix='/api/v1'):
        """Construct an object to access the Canvas API. """
        self.access_token = access_token
        self.api_url = base_url + api_prefix

    def put(self, api_url, payload=None):
        url = self.api_url + api_url

        if payload is None:
            payload = {}

        if self.access_token is not None:
            payload['access_token'] =  self.access_token

        r = requests.put(url, params=payload)

        # raises an exception if there was an http error
        r.raise_for_status()
        return r

    def post(self, api_url, payload=None):
        url = self.api_url + api_url

        if payload is None:
            payload = {}

        if self.access_token is not None:
            payload['access_token'] =  self.access_token

        r = requests.post(url, data=payload)

        # raises an exception if there was an http error
        r.raise_for_status()
        return r



    def get_response(self, url, payload=None):
        if payload is None:
            payload = {}

        if self.access_token is not None:
            payload['access_token'] =  self.access_token

        r = requests.get(url, params=payload)

        # raises an exception if there was an http error
        r.raise_for_status()
        return r

    def get_responses(self, api, payload=None):
        url = self.api_url + api


        # print url
        responses = []
        while True:

            r = self.get_response(url)
            responses.append(r)

            if 'next' in r.links:
                url = r.links['next']['url']
            else:
                break

        return responses

    def get(self, api, to_json=True, payload=None, single=False):

        responses = self.get_responses(api, payload=payload)
        if to_json:
            responses = [r.json() for r in responses]

        if single:
            # print responses
            return responses[0]
        else:
            # print responses
            return list(reduce(lambda x, y: itertools.chain(x, y), responses))

    def get_user(self, user_id):
        return self.get('/users/%s/profile' % user_id, single=True)

    def get_course_groups(self, course_id):
        return self.get('/courses/%s/groups' % course_id)

    def get_group_membership(self, group_id):
        return self.get('/groups/%s/memberships' % group_id)

    def get_courses(self):
        return self.get('/courses')

    def get_assignments(self, course_id):
        return self.get('/courses/%s/assignments' % course_id)

    def get_users(self, course_id):
        return self.get('/courses/%s/users' % course_id)


    def get_quiz_submissions(self, course_id, quiz_id):
        return self.get('/courses/%s/quizzes/%s/submissions' % (course_id, quiz_id))

    def get_assignment_submissions(self, course_id, assignment_id, grouped=False):
        """
        Only returns those submissions that have actually been submitted, rather than potential submissions.
        :param course_id:
        :param assignment_id:
        :return:
        """
        payload = {'grouped': grouped}
        submissions = self.get('/courses/%s/assignments/%s/submissions' % (course_id, assignment_id), payload=payload)
        return filter(lambda sub: sub['workflow_state'] != 'unsubmitted', submissions)

    def grade_assignment_submission(self, course_id, assignment_id, user_id, grade, comment=None):

        payload = {'grade_data[%s][posted_grade]' % user_id: grade}
        if comment is not None:
            payload['grade_data[%s][text_comment]' % user_id] = comment

        return self.post('/courses/%s/assignments/%s/submissions/update_grades' % (course_id, assignment_id), payload=payload)

    def comment_assignment_submission(self, course_id, assignment_id, user_id, comment):

        payload = {'grade_data[%s][text_comment]' % user_id: comment}

        return self.post('/courses/%s/assignments/%s/submissions/update_grades' % (course_id, assignment_id), payload=payload)

    def set_group_name(self, group_id, name):

        payload = {'name': name}
        return self.put('/groups/%s' % (group_id), payload=payload)

    def set_group_membership(self, group_set_builder):
        results = []
        for group_id, membership in group_set_builder.groups.iteritems():
            payload = {}
            payload['members[]'] = membership
            # print payload
            self.put('/groups/%s' % (group_id), payload=payload)
        # return results

    def get_submission_attachments(self, submission, as_bytes=False):
        """
        Get a dictionary containing the attachment files for this submission.
        :param submission: A JSON submission object.
        :param as_bytes: If True, get the file as bytes, else it will be returned as text.
        :return: A dictionary mapping filename to file contents.
        """
        attachments = {}

        if 'attachments' in submission:
            for attachment in submission['attachments']:
                r = requests.get(attachment['url'], params={'access_token': self.access_token})
                if as_bytes:
                    attachments[attachment['filename']] = r.content
                else:
                    attachments[attachment['filename']] = r.text
        return attachments
