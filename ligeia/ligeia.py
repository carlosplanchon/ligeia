#!/usr/bin/env python3

from subprocess import run
from tempfile import NamedTemporaryFile

from playsound import playsound

from servussymtowords import units_and_numbers_to_words
from tokenizesentences import SplitIntoSentences

from sudoaptinstall import sudo_apt_install

from subprocess import CompletedProcess

from typing import Any


def satisfize_dependencies(root_password: str) -> Any:
    """
    Satisfize APT package dependencies.
    :param root_password: str: root password, get it with getpass.getpass

    """
    return sudo_apt_install(
        package_list=["espeak", "libttspico-utils"],
        password=root_password
        )


def say_print(text: str, silent: bool, silent_text: str = "Say: ") -> None:
    """
    Print text to say.
    :param text: str: Text to say.
    :param silent: bool: Silent status.
    :param silent_text: str:  (Default value = "Say: ")

    """
    if silent:
        silent_status = "Silent: True"
    else:
        silent_status = "Silent: False"

    print(f"{silent_text} ({silent_status}) > {text}")
    return None


class eSpeak:
    """
    eSpeakNG, initially released by Jonathan
    Installed on Ubuntu using the package espeak.
    """
    def __convert_lang(self, lang: str) -> str:
        return lang.split("-")[0]

    def say(
        self,
        text: str,
        lang: str = "en",
        default_parameters: str = "-p 30 -a 200",
        user_parameters: str = ""
            ) -> None:
        """
        Say something with eSpeak.
        :param text: str: Text to say.
        :param lang: str: Language (Default value = "en")
        :param default_parameters: str:
            Default parameters to eSpeak. (Default value = "-p 30 -a 200")
        :param user_parameters: str:
            User defined parameters to eSpeak. (Default value = "")

        """
        lang = self.__convert_lang(lang)
        run(
            f"espeak -v {lang} {user_parameters} "
            f'{default_parameters} {text}"',
            shell=True
            )
        return None

    def generate_file(
        self,
        destiny_path: str,
        text: str,
        lang: str = "en",
        default_parameters: str = "-p 30 -a 200",
        user_parameters: str = ""
            ) -> CompletedProcess:
        """
        Generate a wav audio file with eSpeak.
        :param destiny_path: str: Path where the file will be generated.
        :param text: str: Text to synthetize.
        :param lang: str: Language to use. (Default value = "en")
        :param default_parameters: str:
            Default parameters to eSpeak. (Default value = "-p 30 -a 200")
        :param user_parameters: str:
            User-defined parameter to eSpeak. (Default value = "")
        """
        lang = self.__convert_lang(lang)
        return run(
            f"espeak -v {lang} {user_parameters} "
            f'{default_parameters} -w {destiny_path} "{text}"',
            shell=True,
        )


class PicoTTS:
    """
    PicoTTS, released by SVOX.
    SVOX is owned by of Nuance Communications.
    https://en.wikipedia.org/wiki/SVOX
    Installed on Ubuntu using libttspico-utils.
    """
    def say(
        self,
        text: str,
        lang: str = "en-US",
        default_parameters: str = "",
        user_parameters: str = ""
            ) -> None:
        """
        Say something with PicoTTS.
        :param text: str: Text to say.
        :param lang: str: Language (Default value = "en-US")
        :param default_parameters: str:
            Default parameters to PicoTTS. (Default value = "")
        :param user_parameters: str:
            User-defined parameters to PicoTTS. (Default value = "")

        """
        with NamedTemporaryFile(suffix=".wav") as f:
            run(
                f"pico2wave --lang {lang} {default_parameters} "
                f'{user_parameters} --wave {f.name} "{text.lower()}"',
                shell=True,
            )
            playsound(f.name)
        return None

    def generate_file(
        self,
        destiny_path: str,
        text: str,
        lang: str = "en-US",
        default_parameters: str = "",
        user_parameters: str = ""
            ) -> CompletedProcess:
        """
        Generate a wav audio file with PicoTTS.
        :param destiny_path: str: Path where the file will be generated.
        :param text: str: Text to synthetize.
        :param lang: str: Language to use. (Default value = "en-US")
        :param default_parameters: str:
            Default parameters to PicoTTS. (Default value = "")
        :param user_parameters: str:
            User-defined parameter to PicoTTS. (Default value = "")

        """
        return run(
            f"pico2wave {default_parameters} {user_parameters} --lang {lang} "
            f'--wave {destiny_path} "{text.lower()}"',
            shell=True,
        )


class VoiceController:
    """
    It is an abstraction layer capable of working with various voices.

    """
    def __init__(self):
        self.splitsentences_obj = SplitIntoSentences()

    def say(
        self,
        text: str,
        lang: str = "en-US",
        silent: bool = False,
        say_silent: bool = False,
        print_statement: bool = False,
        text_preprocessing: bool = True,
        silent_text: str = "Say",
        ligeia_text: str = "Ligeia > ",
        split_into_sentences: bool = True,
        preprocess_text: bool = True
            ) -> None:
        """
        Say something with loaded voice.

        :param text: str: Text to synthetize.
        :param lang: str: Lang to use. (Default value = "en-US")
        :param silent: bool: Silent voice. (Default value = False)
        :param say_silent: bool: Print text. (Default value = False)
        :param print_statement: bool:  (Default value = False)
        :param text_preprocessing: bool:
            Text preprocessing. (Default value = True)
        :param silent_text: str: Silent say text. (Default value = "Say")
        :param ligeia_text: str: Ligeia text. (Default value = "Ligeia > ")
        :param split_into_sentences: bool:
            Split text inton sentences using tokenizesentences package.
            (Default value = True)
        :param preprocess_text: bool: Preprocess text (text.lower()).
            (Default value = True)
        """

        if text_preprocessing and lang == "en-US":
            text = units_and_numbers_to_words(text)

        if not say_silent:
            say_print(text, silent, silent_text)

        if not silent and text != "":
            if preprocess_text:
                # We preprocess text.
                text = text.lower()
            if split_into_sentences:
                # We split the text to process each statement on his own.
                statement_list = self.splitsentences_obj.split_into_sentences(
                    text=text
                    )
                for statement in statement_list:
                    if print_statement:
                        print(f"{ligeia_text}{statement}")
                    self.selected_voice.say(text=statement, lang=lang)
            else:
                self.selected_voice.say(text=text, lang=lang)
        return None

    def load_voice(self, voice_object: Any) -> None:
        """
        Load a voice.
        :param voice_object: Any: Voice class.

        """
        self.selected_voice = voice_object()
        self.generate_file = self.selected_voice.generate_file
        return None
