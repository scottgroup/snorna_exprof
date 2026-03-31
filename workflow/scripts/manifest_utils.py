"""
Author(s): Alphonse Birane Thiaw
Adapted from MArtin Gautier (AAFC)
"""

import pandas as pd
from typing import List
from os.path import basename
import re


class ManifestHolderSR:
    """Utility class to load the manifest file into a dataframe. For single read (SR) like Nanopore.

    This utility class loads a manifest file, in tsv format, without header, into a Pandas DataFrame.
    It is intented to be used with single read data, like Nanopore (1 fastq/fastq.gz per sample).
    See function `_load_input_file_list` below for the expected tsv file structure.
    """

    _manifest = None

    def _load_input_file_list(self, manifest_filepath: str) -> None:
        """Loads a manifest tsv formatted file into a Pandas DataFrame object.

        Two columns are expected: the first being a sample_id, the second being a filepath to a fastq file.
        Also, no header row should be present in the tsv file.

        Parameters
        ----------
        manifest_filepath: str
            The file path to a tsv input file (like the manifest) with no
            header row.

        Returns
        -------
        pandas.DataFrame
            Returns a pandas.DataFrame created from the TSV file.
        """
        df = pd.read_csv(manifest_filepath, sep="\t", header=None)
        df.columns = ["SAMPLE_ID", "PATH"]
        self._manifest = df

    def get(self):
        return self._manifest

    def get_samples(self) -> List[str]:
        return self.get()["SAMPLE_ID"].to_list()

    def get_sample_fastq_path(self, sample_id: str) -> str:
        data = self.get()
        return data.loc[data.SAMPLE_ID == sample_id, "PATH"].values[0]

    def get_fastq_paths(self) -> List[str]:
        return self.get()["PATH"].to_list()

    def get_fastq_names_prefixes(self) -> List[str]:
        """
        Returns
        -------
        List[str]
            Returns a list of base names for all the fastq.gz files.
        """
        raw_fastqs = self.get_fastq_paths()
        raw_fastqs = [basename(f) for f in raw_fastqs]
        pattern = r'^(.*).fastq.gz'
        d = r'\1'
        raw_fastqs = [re.sub(pattern, d, f, flags=re.DOTALL) for f in raw_fastqs]
        return raw_fastqs

    def __init__(self, manifest_path: str):
        self._load_input_file_list(manifest_path)


class ManifestHolderSRF:
    """Utility class to load the manifest file into a dataframe. For single read folder (SRF) like Nanopore.

    This utility class loads a manifest file, in tsv format, without header, into a Pandas DataFrame.
    It is intented to be used with single read data folders, like Nanopore (one folder per sample, containing
    multiples fastq or fastq.gz files).
    See function `_load_input_folder_list` below for the expected tsv file structure.
    """

    _manifest = None

    def _load_input_folder_list(self, manifest_filepath: str) -> None:
        """Loads a manifest tsv formatted file into a Pandas DataFrame object.

        Two columns are expected: the first being a sample_id, the second being the path to a folder containing
        fastq files. Also, no header row should be present in the tsv file.

        Parameters
        ----------
        manifest_filepath: str
            The file path to a tsv input file (like the manifest) with no
            header row.

        Returns
        -------
        pandas.DataFrame
            Returns a pandas.DataFrame created from the TSV file.
        """
        df = pd.read_csv(filepath_or_buffer=manifest_filepath, sep="\t", header=None)
        df.columns = ["SAMPLE_ID", "PATH"]
        self._manifest = df

    def get(self) -> pd.DataFrame:
        return self._manifest

    def get_sample_folder_path(self, sample_id: str) -> str:
        """
        Parameters
        ----------
        sample_id: str
            The sample id for which to return its folder path

        Returns
        -------
        str
            Returns the folder path for a given sample id
        """
        data = self.get()
        folder_path = data.loc[data.SAMPLE_ID == sample_id, "PATH"].values[0]
        if folder_path == "":
            raise ValueError(f"get_sample_folder_path() for sample id {sample_id} returned an empty string")
        return folder_path

    def get_samples(self) -> List[str]:
        return self.get()["SAMPLE_ID"].to_list()

    def __init__(self, manifest_path: str):
        self._load_input_folder_list(manifest_path)


class ManifestHolderPE:
    """Utility class to load the manifest file into a dataframe. For paired end read (PE) like Illumina MiSeq.

    This utility class loads a manifest file, in tsv format, without header, into a Pandas DataFrame.
    It is intented to be used with paired end read data, like Illumina MiSeq: 2 fastq/fastq.gz per sample (forward +
    reverse reads).
    See function `_load_input_files_list_paired_end` below for the expected tsv file structure.
    """

    _manifest = None

    def _load_input_files_list_paired_end(self, manifest_filepath: str) -> None:
        """Loads a manifest tsv formatted file into a Pandas DataFrame object.

        Three columns are expected: the first being a sample_id, the second being the path to the forward (r1) fastq
        file for that sample, and the third being the path to the reverse (r2) fastq file for that samples.
        Also, no header row should be present in the tsv file.

        Parameters
        ----------
        manifest_filepath: str
            The file path to a tsv input file (like the manifest) with no
            header row.

        Returns
        -------
        pandas.DataFrame
            Returns a pandas.DataFrame created from the TSV file.
        """
        df = pd.read_csv(filepath_or_buffer=manifest_filepath,
                         sep='\t', header=None)
        df.columns = ["SAMPLE_ID", "R1", "R2"]
        self._manifest = df

    def get_pe(self) -> pd.DataFrame:
        return self._manifest

    def get_fastq_path(self, get_forward: bool,
                       sample_id: str) -> str:
        """
        Parameters
        ----------
        get_forward: bool
            If True, returns the filepath of R1, else R2
        sample_id: str
            The sample id for which to return the fastq.gz filepath

        Returns
        -------
        str
            Returns, for a given sample id, the path of the forward or
            reverse fastq.gz, depending on what was requested through
            the get_forward parameter.
        """
        data = self.get_pe()
        if get_forward:
            return data.loc[data.SAMPLE_ID == sample_id, "R1"].values[0]
        else:
            return data.loc[data.SAMPLE_ID == sample_id, "R2"].values[0]

    def get_fastq_paths(self, get_forward: bool) -> List[str]:
        if get_forward:
            return self.get_pe()["R1"].values
        else:
            return self.get_pe()["R2"].values

    def get_samples(self) -> List[str]:
        return self.get_pe()["SAMPLE_ID"]

    def __init__(self, manifest_path: str):
        self._load_input_files_list_paired_end(manifest_path)
