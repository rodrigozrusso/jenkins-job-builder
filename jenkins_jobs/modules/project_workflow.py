# -*- coding: utf-8 -*-
# Copyright 2015 Rodrigo Zacheu Russo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
The Workflow Project module handles creating Workflow Jenkins projects.
You may specify ``workflow`` in the ``project-type`` attribute of
the :ref:`Job` definition.

Requires the Jenkins :jenkins-wiki:`Workflow Plugin 
<https://wiki.jenkins-ci.org/display/JENKINS/Workflow+Plugin>`.

In order to use it for job-template you have to escape the curly braces by
doubling them in the script: { -> {{ , otherwise it will be interpreted by the
python str.format() command.

:Job Parameters:
    * **script** (`str`): The workflow script content.
    * **sandbox** (`str`): The workflow script content. \
    (default false)
    * **sandbox** (`bool`) -- exclude drafts (Default: False)

Job example:

    .. literalinclude::
      /../test/fixtures/project_workflow_001.yaml

Job template example:

    .. literalinclude::
      /../test/fixtures/project_workflow_003.yaml


"""

import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base

class Workflow(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        xml_parent = XML.Element('flow-definition')
        xml_parent.attrib['plugin'] = 'workflow-job'

        definition = XML.SubElement(xml_parent, 'definition')
        definition.attrib['class'] = \
            'org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition'
        definition.attrib['plugin'] = 'workflow-cps'

        if 'script' in data:
            XML.SubElement(definition, 'script').text = data.get('script', '')

            sandbox = data.get('sandbox', False)
            XML.SubElement(definition, 'sandbox').text = str(sandbox).lower()
        elif 'script-path' in data:
            XML.SubElement(definition, 'scriptPath').text = data.get('script-path', '')
            scm = jenkins_jobs.modules.scm.SCM
            print scm
            # for module in self.registry.modules:
              # print module
            # scm_module = self.registry.modules['scm']
            # logger.info(scm_module)
            scm.gen_xml(self, xml_parent, data)


        return xml_parent
