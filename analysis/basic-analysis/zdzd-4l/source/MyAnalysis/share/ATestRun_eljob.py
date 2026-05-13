#!/usr/bin/env python

# Read the submission directory as a command line argument. You can
# extend the list of arguments with your private ones later on.
import optparse
parser = optparse.OptionParser()
parser.add_option( '-s', '--submission-dir', dest = 'submission_dir',
                   action = 'store', type = 'string', default = 'submitDir',
                   help = 'Submission directory for EventLoop' )
( options, args ) = parser.parse_args()

# Set up (Py)ROOT.
import ROOT
ROOT.xAOD.Init().ignore()

# Set up the sample handler object. See comments from the C++ macro
# for the details about these lines.
sh = ROOT.SH.SampleHandler()
sh.setMetaString( 'nc_tree', 'CollectionTree' )
inputFilePath = '/eos/atlas/atlascerngroupdisk/phys-hmbs/hlrs/ZdZd/signal_sample_generator/automatedSignalGenerator/new_HAHM/ZZ_4l_mH500.0_mS413.0_mZd30.0/'

print('Variable type is:', inputFilePath)
# ROOT.SH.ScanDir().filePattern( 'DAOD_TRUTH1.truth1.root' ).scan( sh, inputFilePath )
ROOT.SH.ScanDir().filePattern( 'DAOD_TRUTH1.truthDAOD_ZZ_mS413_mZd30.pool.root' ).scan( sh, inputFilePath )
sh.printContent()

# Create an EventLoop job.
job = ROOT.EL.Job()
job.sampleHandler( sh )
job.options().setDouble( ROOT.EL.Job.optMaxEvents, 10000 )
job.options().setString( ROOT.EL.Job.optSubmitDirMode, 'unique-link')

# Create the algorithm's configuration.
from AnaAlgorithm.DualUseConfig import createAlgorithm
alg = createAlgorithm ( 'MyxAODAnalysis', 'AnalysisAlg' )

# later on we'll add some configuration options for our algorithm that go here

# Add our algorithm to the job
job.algsAdd( alg )

# Run the job using the direct driver.
driver = ROOT.EL.DirectDriver()
driver.submit( job, options.submission_dir )


