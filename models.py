import os

from django.db import models
from django.conf import settings


class CustomStyling(models.Model):
	journal = models.ForeignKey('journal.Journal')
	css = models.TextField(
		blank=True,
		null=True,
		verbose_name="Custom CSS",
	)

	def write_to_disk(self):
		path = os.path.join(
			settings.MEDIA_ROOT,
			'customstyling',
			str(self.journal.pk),
		)
		file = os.path.join(path, 'custom.css')
		if not os.path.exists(path):
			os.makedirs(path)

		with open(file, 'w') as css_file:
			css_file.write(self.css)
			css_file.close()

	def url(self):
		return '{}customstyling/{}/custom.css'.format(
			settings.MEDIA_URL,
			self.journal.pk,
		)
