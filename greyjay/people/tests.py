from django.test import TestCase
from django.utils import six

from . import models


class ContributorPageTestCase(TestCase):
    fixtures = ["people_test.json", ]

    def _copy_values_from_fixture(self, pk, new_contributor):
        # TODO: This is EXTERMELY hacky - we have to re-engineer our tests...
        fixed_contributor = models.ContributorPage.objects.get(pk=pk)
        new_contributor.path = fixed_contributor.path + '1'
        new_contributor.slug = fixed_contributor.slug
        new_contributor.title = fixed_contributor.title
        return new_contributor

    def test_str_returns_name_and_email(self):
        contributor = models.ContributorPage(first_name="Bob", last_name="Smith", email="bob@example.com")

        self.assertEqual(str(contributor), "Bob Smith - bob@example.com")

    def test_full_name_returns_first_and_last_name(self):
        contributor = models.ContributorPage(first_name="Bob", last_name="Smith", email="bob@example.com")

        self.assertEqual(contributor.full_name, "Bob Smith")

    def test_last_comma_first_name_returns_last_name_and_first_name(self):
        contributor = models.ContributorPage(first_name="Bob", last_name="Smith", email="bob@example.com")

        self.assertEqual(contributor.last_comma_first_name, "Smith, Bob")

    def test_twitter_handle_has_at_when_not_specified(self):
        contributor = models.ContributorPage(first_name="Bob", last_name="Smith", depth=1, twitter_handle="bob")
        contributor = self._copy_values_from_fixture(12, contributor)
        contributor.save()
        self.assertEqual(contributor.twitter_handle, "@bob")

    def test_twitter_handle_has_at_when_specified(self):
        contributor = models.ContributorPage(first_name="Bob", last_name="Smith", depth=1, twitter_handle="@bob")
        contributor = self._copy_values_from_fixture(12, contributor)
        contributor.save()
        self.assertEqual(contributor.twitter_handle, "@bob")

    def test_twitter_handle_not_modified_if_not_specified(self):
        contributor = models.ContributorPage(first_name="Bob", last_name="Smith", depth=1)
        contributor = self._copy_values_from_fixture(12, contributor)
        contributor.save()
        self.assertEqual(contributor.twitter_handle, "")

    def test_display_twitter_handle_does_not_contain_at(self):
        contributor = models.ContributorPage(first_name="Bob", last_name="Smith", depth=1, twitter_handle="@bob")
        contributor = self._copy_values_from_fixture(12, contributor)
        contributor.save()
        self.assertEqual(contributor.display_twitter_handle, "bob")


class ContributorListPageTestCase(TestCase):
    fixtures = ["people_test.json", ]

    def test_str_returns_title(self):
        contributor_list = models.ContributorListPage(title="This is the title.")
        self.assertEqual(str(contributor_list), "This is the title.")

    def test_list_of_contributors_contains_all_live_contributors(self):
        contributor_list = models.ContributorListPage.objects.all().first()
        all_live_contributors = models.ContributorPage.objects.live()

        six.assertCountEqual(
            self,
            all_live_contributors,
            contributor_list.nonfeatured_contributors[0]
        )

    def test_list_of_contributors_sorted_by_last_name(self):
        contributor_list = models.ContributorListPage.objects.all().first()
        contributors = contributor_list.nonfeatured_contributors

        joe = models.ContributorPage.objects.get(slug="joe-sampson")
        beth = models.ContributorPage.objects.get(slug="beth-smith")
        bob = models.ContributorPage.objects.get(slug="bob-smith")
        mary = models.ContributorPage.objects.get(slug="mary-sue")

        self.assertSequenceEqual(contributors, [[joe, beth, bob, mary]])
