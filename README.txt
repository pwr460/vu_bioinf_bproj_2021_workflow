Instructions for running vu_bioinf_bproj_2021_workflow
Date of writing: 17-06-2021
-------------------------------------------------------------------------------------------------------------------------------------------------------------
Location: /scistor/informatica/pwr460/vu_bioinf_bproj_2021_workflow
Zip Location: /scistor/informatica/pwr460/vu_bioinf_bproj_2021_workflow.zip
-------------------------------------------------------------------------------------------------------------------------------------------------------------
Instructions:

1. Edit workflow_script.sh to run workflow with on correct dataset(s) 

	option 1:
		- replace value of the 'dsf' flag with the location of the super dict where your datasets are located.
		- replace value of 'ds' flag with a list of datasets. *the names of these datasets should match a folder in the super dict specified in the 'dsf' flag.
		
		example: 
			given the following dataset folders:
				- mydatasetlocation/mydataset1
				- mydatasetlocation/mydataset2

			set the flags as follows:
				-dsf  mydatasetlocation
				- ds [mydataset1,mydataset2]

	option 2: 
		- replace value of 'ds' flag with a list of dataset locations.
		- leave out 'dsf' flag

		example: 
			given the following dataset folders:
				- mydatasetlocation1/mydataset1
				- mydatasetlocation2/mydataset2

			set the flags as follows:
				- ds [mydatasetlocation1/mydataset1,mydatasetlocation2/mydataset2]



2. Adjust config values in the appsettings.json file

*Most configuration values do not have to be adjusted and are self explanitory. A few note-worthy values will be described however.

	-run_jobs: list of jobs to run. Possible values: "hhblits", "opus_tass", "opus_tass_train"
	-hhblits.database: location of the database to use when running hhblits	
	-hhblits.output_folder: output location of hhblits
	-opus_tass.psi_blast_folder: location of the dataset folders containing the .pssm files used by OPUS-TASS
	-opus_tass.hhblits_folder: location of the dataset folders containing the .hhm files used by OPUS-TASS
	-opus_tass.output_folder: output location of opus_tass
	-opus_tass.training: configurations for training opus_tass

*remarks:
	- When running hhblits and opus_tass, make sure that hhblits.output_folder holds the same value as opus_tass.hhblits_folder
	- When running running opus_tass with preexisting hhm or pssm datasets, make sure to specify opus_tass.hhblits_folder or opus_tass.psi_blast_folder in the same
	  way the 'dsf' flag was specified in. In other words, the location specified should contain a subfolder for each dataset to run. These subfolders should be named
	  in correspondence with the datasets. The .hhm or .pssm files should be located in these subfolders.

		example:
			- opus_tass.psi_blast_folder = "/mypssmsuperfolder"
			- 'ds' flag is set to [mydataset1]

			then the program will look for .pssm files in /mypssmsuperfolder/mydataset1 when running OPUS-TASS for mydataset1



3. Ensure a valid model is located in the model/ directory
	-The models located in here are used to run opus_tass. When no model is present, the 'opus_tass_train' job can be run in order to create these models.
	-'opus_tass_train' will always output to the model/ directory, this cannot be configured at the time of writing.
	-'opus_tass_train' can be run alongside other jobs in the workflow. It will always be run before the 'opus_tass' job, if specified in the 'run_job' config value.
	-When multiple models are located in the model/ directory, an enclave of these models will be used to run OPUS-TASS.

*At the time of writing, the 'opus_tass_train' job is poorly optimised, taking a vast amount of time to complete. It is recommended to generate the models for OPUS-TASS
 using the OPUS-TASS code directly and not this workflow.



4. Run/submit workflow_script.sh 

*Note, this script should be run from the vu_bioinf_bproj_2021_workflow/ directory, if run from elsewhere, make sure to insert a 'cd' command in the script.
 This command must be inserted before the following line: "source ./venv/bin/activate"

-------------------------------------------------------------------------------------------------------------------------------------------------------------
Output:

The default output location is "vu_bioinf_bproj_2021_workflow/results/opus_tass". This can be changed in the appsettings.json file.
For each dataset run, a subfolder will be made in the output directory. This folder matches the name of the dataset.
Outputs are generated for each .fasta file, in the form of a .opus file.
The output of hhblits is stored as well, being located in the "vu_bioinf_bproj_2021_workflow/results/hhblits" dictionary by default, utilizing a similar structure as the OPUS-TASS output
 


