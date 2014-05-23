# -*- coding: utf-8 -*-
"Test for Annotation Xmodule functional logic."

import unittest
from mock import Mock
from lxml import etree

from xblock.field_data import DictFieldData
from xblock.fields import ScopeIds

from xmodule.videoannotation_module import VideoAnnotationModule

from . import get_test_system


class VideoAnnotationModuleTestCase(unittest.TestCase):
    ''' Video Annotation Module Test Case '''
    sample_xml = '''
        <annotatable>
            <instructions><p>Video Test Instructions.</p></instructions>
        </annotatable>
    '''
    sample_sourceurl = "http://video-js.zencoder.com/oceans-clip.mp4"
    sample_youtubeurl = "http://www.youtube.com/watch?v=yxLIu-scR9Y"

    def setUp(self):
        """
        Makes sure that the Video Annotation Module is created.
        """
        self.mod = VideoAnnotationModule(
            Mock(),
            get_test_system(),
            DictFieldData({'data': self.sample_xml, 'sourceUrl': self.sample_sourceurl}),
            ScopeIds(None, None, None, None)
        )

    def test_extract_instructions(self):
        """
        This test ensures that if an instruction exists it is pulled and
        formatted from the <instructions> tags. Otherwise, it should return nothing.
        """
        xmltree = etree.fromstring(self.sample_xml)

        expected_xml = u"<div><p>Video Test Instructions.</p></div>"
        actual_xml = self.mod._extract_instructions(xmltree)  # pylint: disable=W0212
        self.assertIsNotNone(actual_xml)
        self.assertEqual(expected_xml.strip(), actual_xml.strip())

        xmltree = etree.fromstring('<annotatable>foo</annotatable>')
        actual = self.mod._extract_instructions(xmltree)  # pylint: disable=W0212
        self.assertIsNone(actual)

    def test_get_extension(self):
        """
        Tests the function that returns the appropriate extension depending on whether it is
        a video from youtube, or one uploaded to the EdX server.
        """
        expectedyoutube = 'video/youtube'
        expectednotyoutube = 'video/mp4'
        result1 = self.mod._get_extension(self.sample_sourceurl)  # pylint: disable=W0212
        result2 = self.mod._get_extension(self.sample_youtubeurl)  # pylint: disable=W0212
        self.assertEqual(expectedyoutube, result2)
        self.assertEqual(expectednotyoutube, result1)

    def test_get_html(self):
        """
        Tests to make sure variables passed in truly exist within the html once it is all rendered.
        """
        context = self.mod.get_html()
        for key in ['display_name', 'instructions_html', 'sourceUrl', 'typeSource', 'poster', 'annotation_storage']:
            self.assertIn(key, context)
