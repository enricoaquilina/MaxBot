from selenium import webdriver
import  os
from time import sleep


class  zapbot :
    # Our script's execution location
    dir_path = os.getcwd()
    # The chromedriver path
    chromedriver = os.path.join(dir_path, "chromedriver.exe")
    # Path where profile folder will be created
    profile = os.path.join(dir_path, "profile", "wpp")

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # Configuring the profile folder, to keep the section data
        self.options.add_argument(
            r"user-data-dir={}".format(self.profile))
        # Initializes the webdriver
        self.driver = webdriver.Chrome(
            self.chromedriver, chrome_options=self.options)
        # Open or whatsappweb
        self.driver.get("https://web.whatsapp.com/")
        # Wait a few seconds for QrCode manual validation
        self.driver.implicitly_wait(15)

    def stop(self):
        self.driver.quit()

    def ultima_msg(self):
        """ Captura a ultima mensagem da conversa """
        try:
            post = self.driver.find_elements_by_class_name("_3_7SH")
            ultimo  =  len ( post ) -  1
            # The text of the last message
            texto = post[ultimo].find_element_by_css_selector(
                "span.selectable-text").text
            return texto
        except Exception as e:
            print ( "Error reading msg, trying again!" )

    def envia_msg(self, msg):
        "" "Sends a message to the open conversation" ""
        try:
            sleep(2)
            # Select the message box
            self.message_box = self.driver.find_elements_by_class_name("_2S1VP")
            self.message_box[1].click()
            # Type the message
            self.message_box[1].send_keys(msg)
            sleep(1)
            # Select send button
            self.botao_enviar = self.driver.find_element_by_class_name("_35EW6")
            # Send msg
            self.botao_enviar.click()
            sleep(2)
        except Exception as e:
            print ( "Error sending message" , e )

    def envia_media(self, fileToSend):
        """ Envia media """
        try:
            # Click the add button
            self.driver.find_element_by_css_selector("span[data-icon='clip']").click()
            # Select input
            attach = self.driver.find_element_by_css_selector("input[type='file']")
            # Add file
            attach.send_keys(fileToSend)
            sleep(3)
            # Select send button
            send = self.driver.find_element_by_xpath("//div[contains(@class, 'yavlE')]")
            # Click the send button
            send.click()
        except Exception as e:
            print ( "Error sending media" , e )

    def  open_conversation ( self , contact ):
        "" "Open the conversation with a specific contact" ""
        try:
            # Select the conversation search box
            self.search_box = self.driver.find_element_by_class_name("_2S1VP")
            # Enter the contact name or number
            self.search_box.send_keys ( contact )
            sleep(2)
            # Select contact
            self.contato = self.driver.find_element_by_xpath("//span[@title = '{}']".format(contact))
            # Join the conversation
            self.contato.click()
        except Exception as e:
            raise e


bot  =  zapbot()
bot.open_conversation("Pukkad")
bot.envia_msg( "how's it going?" )
bot.stop()
image  =  bot.dir_path  +  "/imagem.jpg"
msg = ""
# while msg != "/quit":
#     sleep(1)
#     msg  =  bot.ultima_msg()
#     if msg == "/help":
#         bot.envia_msg( "" "Bot: This is text with valid commands:/ help (for help)/ more (to find out more)/ quit (to exit)""")
#     elif  msg  ==  "/ but" :
#         bot.envia_media( image )
#     elif msg == "/quit":
#         bot.envia_msg("Bye bye!")