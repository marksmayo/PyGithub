############################ Copyrights and license ############################
#                                                                              #
# Copyright 2012 Vincent Jacques <vincent@vincent-jacques.net>                 #
# Copyright 2012 Zearin <zearin@gonk.net>                                      #
# Copyright 2013 AKFish <akfish@gmail.com>                                     #
# Copyright 2013 Michael Stead <michael.stead@gmail.com>                       #
# Copyright 2013 Vincent Jacques <vincent@vincent-jacques.net>                 #
# Copyright 2014 Vincent Jacques <vincent@vincent-jacques.net>                 #
# Copyright 2016 Jannis Gebauer <ja.geb@me.com>                                #
# Copyright 2016 Peter Buckley <dx-pbuckley@users.noreply.github.com>          #
# Copyright 2017 Nicolas Agustín Torres <nicolastrres@gmail.com>               #
# Copyright 2018 Wan Liuyang <tsfdye@gmail.com>                                #
# Copyright 2018 per1234 <accounts@perglass.com>                               #
# Copyright 2018 sfdye <tsfdye@gmail.com>                                      #
# Copyright 2020 Huan-Cheng Chang <changhc84@gmail.com>                        #
#                                                                              #
# This file is part of PyGithub.                                               #
# http://pygithub.readthedocs.io/                                              #
#                                                                              #
# PyGithub is free software: you can redistribute it and/or modify it under    #
# the terms of the GNU Lesser General Public License as published by the Free  #
# Software Foundation, either version 3 of the License, or (at your option)    #
# any later version.                                                           #
#                                                                              #
# PyGithub is distributed in the hope that it will be useful, but WITHOUT ANY  #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS    #
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more #
# details.                                                                     #
#                                                                              #
# You should have received a copy of the GNU Lesser General Public License     #
# along with PyGithub. If not, see <http://www.gnu.org/licenses/>.             #
#                                                                              #
################################################################################

import github.GithubObject
import github.NamedUser

from . import Consts


class IssueComment(github.GithubObject.CompletableGithubObject):
    """
    This class represents IssueComments. The reference can be found here https://docs.github.com/en/rest/reference/issues#comments
    """

    def __repr__(self):
        return self.get__repr__({"id": self._id.value, "user": self._user.value})

    @property
    def body(self):
        """
        :type: string
        """
        self._completeIfNotSet(self._body)
        return self._body.value

    @property
    def created_at(self):
        """
        :type: datetime.datetime
        """
        self._completeIfNotSet(self._created_at)
        return self._created_at.value

    @property
    def id(self):
        """
        :type: integer
        """
        self._completeIfNotSet(self._id)
        return self._id.value

    @property
    def issue_url(self):
        """
        :type: string
        """
        self._completeIfNotSet(self._issue_url)
        return self._issue_url.value

    @property
    def updated_at(self):
        """
        :type: datetime.datetime
        """
        self._completeIfNotSet(self._updated_at)
        return self._updated_at.value

    @property
    def url(self):
        """
        :type: string
        """
        self._completeIfNotSet(self._url)
        return self._url.value

    @property
    def html_url(self):
        """
        :type: string
        """
        self._completeIfNotSet(self._html_url)
        return self._html_url.value

    @property
    def user(self):
        """
        :type: :class:`github.NamedUser.NamedUser`
        """
        self._completeIfNotSet(self._user)
        return self._user.value

    def delete(self):
        """
        :calls: `DELETE /repos/{owner}/{repo}/issues/comments/{id} <https://docs.github.com/en/rest/reference/issues#comments>`_
        :rtype: None
        """
        headers, data = self._requester.requestJsonAndCheck("DELETE", self.url)

    def edit(self, body):
        """
        :calls: `PATCH /repos/{owner}/{repo}/issues/comments/{id} <https://docs.github.com/en/rest/reference/issues#comments>`_
        :param body: string
        :rtype: None
        """
        assert isinstance(body, str), body
        post_parameters = {
            "body": body,
        }
        headers, data = self._requester.requestJsonAndCheck(
            "PATCH",
            self.url,
            input=post_parameters,
        )
        self._useAttributes(data)

    def get_reactions(self):
        """
        :calls: `GET /repos/{owner}/{repo}/issues/comments/{id}/reactions
                <https://docs.github.com/en/rest/reference/reactions#list-reactions-for-an-issue-comment>`_
        :return: :class: :class:`github.PaginatedList.PaginatedList` of :class:`github.Reaction.Reaction`
        """
        return github.PaginatedList.PaginatedList(
            github.Reaction.Reaction,
            self._requester,
            f"{self.url}/reactions",
            None,
            headers={"Accept": Consts.mediaTypeReactionsPreview},
        )

    def create_reaction(self, reaction_type):
        """
        :calls: `POST /repos/{owner}/{repo}/issues/comments/{id}/reactions
                <https://docs.github.com/en/rest/reference/reactions#create-reaction-for-an-issue-comment>`_
        :param reaction_type: string
        :rtype: :class:`github.Reaction.Reaction`
        """
        assert isinstance(reaction_type, str), reaction_type
        post_parameters = {
            "content": reaction_type,
        }
        headers, data = self._requester.requestJsonAndCheck(
            "POST",
            f"{self.url}/reactions",
            input=post_parameters,
            headers={"Accept": Consts.mediaTypeReactionsPreview},
        )
        return github.Reaction.Reaction(self._requester, headers, data, completed=True)

    def delete_reaction(self, reaction_id):
        """
        :calls: `DELETE /repos/{owner}/{repo}/issues/comments/{comment_id}/reactions/{reaction_id}
                <https://docs.github.com/en/rest/reference/reactions#delete-an-issue-comment-reaction>`_
        :param reaction_id: integer
        :rtype: bool
        """
        assert isinstance(reaction_id, int), reaction_id
        status, _, _ = self._requester.requestJson(
            "DELETE",
            f"{self.url}/reactions/{reaction_id}",
            headers={"Accept": Consts.mediaTypeReactionsPreview},
        )
        return status == 204

    def _initAttributes(self):
        self._body = github.GithubObject.NotSet
        self._created_at = github.GithubObject.NotSet
        self._id = github.GithubObject.NotSet
        self._issue_url = github.GithubObject.NotSet
        self._updated_at = github.GithubObject.NotSet
        self._url = github.GithubObject.NotSet
        self._html_url = github.GithubObject.NotSet
        self._user = github.GithubObject.NotSet

    def _useAttributes(self, attributes):
        if "body" in attributes:  # pragma no branch
            self._body = self._makeStringAttribute(attributes["body"])
        if "created_at" in attributes:  # pragma no branch
            self._created_at = self._makeDatetimeAttribute(attributes["created_at"])
        if "id" in attributes:  # pragma no branch
            self._id = self._makeIntAttribute(attributes["id"])
        if "issue_url" in attributes:  # pragma no branch
            self._issue_url = self._makeStringAttribute(attributes["issue_url"])
        if "updated_at" in attributes:  # pragma no branch
            self._updated_at = self._makeDatetimeAttribute(attributes["updated_at"])
        if "url" in attributes:  # pragma no branch
            self._url = self._makeStringAttribute(attributes["url"])
        if "html_url" in attributes:  # pragma no branch
            self._html_url = self._makeStringAttribute(attributes["html_url"])
        if "user" in attributes:  # pragma no branch
            self._user = self._makeClassAttribute(
                github.NamedUser.NamedUser,
                attributes["user"],
            )
