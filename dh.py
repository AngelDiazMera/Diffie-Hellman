import random

class Cliente(object):
    # Constructor
    def __init__(self, nombre, primo, generador):
        self.__nombre = nombre # Nombre del cliente
        self.__primo = primo # Número p
        self.__generador = generador # Número g
        self.__llave_priv = self.__generar_llave_priv() # Llave privada
        self.__llave_pub = self.__generar_llave_pub() # Llave pública
        self.__llave_secr = None
        self.__msg_recibido = ""
        print('\tCliente "{}" generado con la llave privada "{}" y la llave pública "{}"'.format(self.__nombre, self.__llave_priv, self.__llave_pub))

    # Llave privada para la persona
    def __generar_llave_priv(self):
        return random.randint(0, self.__primo)

    # Llave generada para la persona
    def __generar_llave_pub(self):
        return int(pow(self.__generador, self.__llave_priv, self.__primo))

    def enviar_msg(self, msg, desti):
        # Para obtener la llave secreta del destinatario K{ab}
        secreta = int(pow(desti.llave_pub, self.__llave_priv, self.__primo ))
        # Aplicar la función HASH SHA-256
        secreta_hash = hashlib.sha256(str(secreta).encode()).hexdigest()
        print('''\tComparando las claves...
         | {}: {}
         | {}: {}'''.format(self.__nombre, self.__llave_secr, desti.nombre, secreta_hash))
        # Compara las llaves K{ab}
        if (self.__llave_secr == secreta_hash):
            print('\tLa clave de {} coincide con la de {}'.format(desti.nombre, self.__nombre))
            desti.msg_recibido = msg
            print('\tEl mensaje "{}" de {} para {} se ha enviado correctamente'.format(msg, self.__nombre, desti.__nombre))
        else:
            raise Exception("Las claves no son iguales")

    def generar_llave_sec(self, llave_pub_otro): # el parámetro es la llave generada de la otra persona
        secreta = int(pow(llave_pub_otro, self.__llave_priv, self.__primo))
        secreta_hash = hashlib.sha256(str(secreta).encode()).hexdigest()
        self.__llave_secr = secreta_hash

    @property
    def llave_pub(self):
        return self.__llave_pub

    @property
    def nombre(self):
        return self.__nombre

    @property
    def msg_recibido(self):
        return self.__msg_recibido

    @msg_recibido.setter
    def msg_recibido(self, msg):
        self.__msg_recibido = msg

# EJECUCUCIÓN DEL PROGRAMA
g = 2  # Generador
p = 23 # Número primo para g = 2

print('''Parámetros de comunicación
\tg = {}
\tp = {}\n'''.format(g, p))

print('Generación de los clientes')
alice = Cliente('Alice', p, g)
bob   = Cliente('Bob',   p, g)
# Generación de las llaves secretas (Establecer comunicación )
print('\nEstableciendo comunicación entre ambos clientes...')
alice.generar_llave_sec(bob.llave_pub) # x_a
bob.generar_llave_sec(alice.llave_pub) # x_b
# Descomentar para prueba del error
# bob.generar_llave_sec(5) # x_b

# Simulación de envío de mensajes
# Mensaje de Alice para Bob
c_a = 'Hola, Bob. De alice'
# Mensaje de Bob para Alice
c_b = 'Hola, Alice. De bob'

print('\n{} envía el mensaje "{}" a {}'.format(alice.nombre, c_a, bob.nombre))
try:
    alice.enviar_msg( c_a, bob )
except Exception as error:
    print('Hubo un error con la transmisión del mensaje: {}'.format(error))

print('\n{} envía el mensaje "{}" a {}'.format(bob.nombre, c_b, alice.nombre))
try:
    bob.enviar_msg( c_b, alice )
except Exception as error:
    print('Hubo un error con la transmisión del mensaje: {}'.format(error))