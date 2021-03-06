'''
   pyecc - Copyright 2009 Slide, Inc.
 
  This library is free software; you can redistribute it and/or 
  modify it under the terms of the GNU Lesser General Public License 
  as published by the Free Software Foundation; either version 2.1 of 
  the License, or (at your option) any later version.
 
  This library is distributed in the hope that it will be useful, 
  but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY 
  or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License 
  for more details. 
 
  You should have received a copy of the GNU Lesser General Public License 
  along with this library; if not, write to the 
  Free Software Foundation, Inc., 
  59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
'''

import _pyecc

DEFAULT_CURVE = _pyecc.DEFAULT_CURVE

class ECC(object):
    '''
        The ECC object must be instantiated to work with
        any encrypted data, as some amount of state is required
        at once
    '''
    def __init__(self, *args, **kwargs):
        self._private = kwargs.get('private')
        self._public = kwargs.get('public')
        self._curve = kwargs.get('curve')
        self._state = _pyecc.new_state()
        self._kp = _pyecc.new_keypair(self._public, self._private, self._state)

    @classmethod
    def generate(cls):
        keys = _pyecc.keygen()
        if keys:
            return cls(public=keys[0], private=keys[1], curve=keys[2])
        return None


    def encrypt(self, plaintext):
        return _pyecc.encrypt(plaintext, self._kp, self._state)

    def decrypt(self, ciphertext):
        assert ciphertext, 'You cannot decrypt "nothing"'
        return _pyecc.decrypt(ciphertext, self._kp, self._state)

    def sign(self, data):
        if not self._kp:
            print 'You need a keypair object to verify a signature'
            return False

        if not self._state:
            print 'ECC object should have an internal _state member'
            return False

        return _pyecc.sign(data, self._kp, self._state)

    def verify(self, data, signature):
        if not self._kp:
            print 'You need a keypair object to verify a signature'
            return False

        if not self._state:
            print 'ECC object should have an internal _state member'
            return False

        return _pyecc.verify(data, signature, self._kp, self._state)
