# coding: utf-8

import mock
import pytest

from django.shortcuts import resolve_url

from factories import ProjectFactory, ChangelogFactory
from projects.models import Project, Changelog


@pytest.mark.django_db
class TestProjectViews(object):
    project_list_url = resolve_url('projects:project_list')
    project_create_url = resolve_url('projects:project_create')

    def test_ping(self, logged_client):
        response = logged_client.get(self.project_list_url)
        assert 200 == response.status_code

    def test_project_list(self, logged_client, account):
        projects = ProjectFactory.create_batch(5)
        projects[0].members.add(account)

        response = logged_client.get(self.project_list_url)

        for project in projects:
            assert str(project.name) in response.content

    def test_add_project(self, logged_client):
        payload = {
            'name': 'Test',
            'description': 'Test Description',
            'tags': 'python, site'
        }

        response = logged_client.post(
            self.project_create_url,
            payload,
            follow=True
        )

        redirect_url, status_code = response.redirect_chain[0]

        assert self.project_list_url in redirect_url
        assert 302 == status_code

        project = Project.objects.get()

        assert 'Test' == project.name
        assert 'Test Description' == project.description


@pytest.mark.django_db
class TestChangelogViews(object):

    def test_add_changelog_without_sending_email(self, logged_client):
        project = ProjectFactory.create()
        changelog_create_url = resolve_url(
            'projects:changelog_add',
            project.pk
        )
        project_detail_url = resolve_url(
            'projects:project_detail',
            project.pk
        )

        payload = {'description': '# version 0.0.1'}

        response = logged_client.post(
            changelog_create_url,
            payload,
            follow=True
        )

        redirect_url, status_code = response.redirect_chain[0]
        assert project_detail_url in redirect_url
        assert status_code == 302

    def test_add_changelog_sending_email(self, logged_client):
        project = ProjectFactory.create()
        changelog_create_url = resolve_url(
            'projects:changelog_add',
            project.pk
        )
        project_detail_url = resolve_url(
            'projects:project_detail',
            project.pk
        )

        payload = {
            'description': '# version 0.0.1',
            'send_mail': True,
            'email_subject': 'Changelog - test',
            'email_recipients': 'luanpab@gmail.com',
        }

        response = logged_client.post(
            changelog_create_url,
            payload,
            follow=True
        )

        redirect_url, status_code = response.redirect_chain[0]
        changelog = Changelog.objects.last()

        assert project_detail_url in redirect_url
        assert status_code == 302

        assert changelog.email_sent

    def test_update_changelog_ok(self, logged_client):
        changelog = ChangelogFactory.create()
        changelog_update_url = resolve_url(
            'projects:changelog_update',
            changelog.pk
        )
        project_detail_url = resolve_url(
            'projects:project_detail',
            changelog.project.pk
        )

        # test GET
        response = logged_client.get(changelog_update_url)
        assert response.status_code == 200

        # test POST
        payload = {'description': '# version 0.0.1'}
        response = logged_client.post(
            changelog_update_url,
            payload,
            follow=True
        )
        redirect_url, status_code = response.redirect_chain[0]

        assert project_detail_url in redirect_url
        assert status_code == 302

    def test_update_changelog_404(self, logged_client):
        changelog = ChangelogFactory.create()
        changelog.email_sent = True
        changelog.save()

        changelog_update_url = resolve_url(
            'projects:changelog_update',
            changelog.pk
        )

        # test GET
        response = logged_client.get(changelog_update_url)
        assert response.status_code == 404

    def test_send_email_ok(self, logged_client):
        changelog = ChangelogFactory.create()
        changelog_send_mail_url = resolve_url(
            'projects:changelog_send_mail',
            changelog.pk
        )
        project_detail_url = resolve_url(
            'projects:project_detail',
            changelog.project.pk
        )

        assert changelog.email_sent is False

        response = logged_client.post(
            changelog_send_mail_url,
            follow=True
        )

        redirect_url, status_code = response.redirect_chain[0]

        assert project_detail_url in redirect_url
        assert status_code == 302

        changelog = Changelog.objects.last()
        assert changelog.email_sent

    def test_send_email_ok_already_sent(self, logged_client):
        changelog = ChangelogFactory.create()
        changelog.email_sent = True
        changelog.save()

        changelog_send_mail_url = resolve_url(
            'projects:changelog_send_mail',
            changelog.pk
        )

        project_detail_url = resolve_url(
            'projects:project_detail',
            changelog.project.pk
        )

        assert changelog.email_sent

        response = logged_client.post(changelog_send_mail_url, follow=True)
        redirect_url, status_code = response.redirect_chain[0]

        assert project_detail_url in redirect_url
        assert status_code == 302

    @mock.patch('projects.models.Changelog.send_slack')
    def test_send_slack_ok(self, slack_mock, logged_client):
        changelog = ChangelogFactory.create()
        changelog_send_slack = resolve_url(
            'projects:changelog_send_slack',
            changelog.pk
        )
        project_detail_url = resolve_url(
            'projects:project_detail',
            changelog.project.pk
        )

        payload = {
            'channel': '#test-channel, #test-slack'
        }

        response = logged_client.post(
            changelog_send_slack,
            payload,
            follow=True
        )

        assert slack_mock.call_count == 2
        assert slack_mock.called

        redirect_url, status_code = response.redirect_chain[0]

        assert project_detail_url in redirect_url
        assert status_code == 302
