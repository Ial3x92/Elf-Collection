The PS4 Dev Wiki has some information on [PKGs](https://www.psdevwiki.com/ps4/PKG_files) and [PFS images](https://www.psdevwiki.com/ps4/PFS). Also check out flatz's [write-up](https://playstationhax.xyz/flatz/) on Fake PKGs.

Anyway, here's some information about PKGs I've discovered in making this library and toolset.

# PKG Encryption
## Developer-controlled keys
The contents of a PKG are encrypted with keys derived from a developer-specified passcode and the Content ID.

Let's call these derived keys dk0 to dk6 based on the index value used to create them.

![Diagram illustrating how the Content Id, Passcode, and an integer index 0 to 6 are hashed with SHA256 to create the derived keys](https://i.imgur.com/bWxtfA6.png)

- dk1 is what flatz/sony refer to as EKPFS. It is used to generate PFS encryption and signing keys.
- dk2 is used to generate the AES iv/key to encrypt the license.info in the PKG entry filesystem.
- dk3 is used to generate the AES iv/key to encrypt the IMAGE_KEY entry, the license.dat, and to encrypt the PKG header signature.
- It is not known if the other derived keys are used for anything. They can be used to encrypt entries in the PKG entry filesystem, but so far I've only seen dk2 and dk3 used for that.

## PFS Key Generation
![Diagram illustrating how XTS and signing keys are created for PFS using HMAC-SHA256](https://i.imgur.com/YesNipe.png)

To generate keys for PFS, the PFS key seed is combined with an index and then hashed with HMAC-SHA256 using the dk1 (EKPFS) as a key. Index 1 generates XTS tweak and data keys, while index 2 generates the HMAC-SHA256 signing key.

## The ENTRY_KEYS entry
![A diagram explaining how the passcode and derived keys are encrypted with RSA and stored in the ENTRY_KEYS entry](https://i.imgur.com/3PLyZSi.png)

6 of the derived keys are encrypted using public-key RSA and stored in the ENTRY_KEYS entry. Their digests are also stored there.
Each derived key gets encrypted with a unique RSA key. The passcode is stored in place of dk0 and it gets its own RSA key as well.
We only have public moduli for these RSA keys; except RSA Key 3, for which we have the public and private keys. This entry is stored unencrypted in the PKG, so to access the passcode, for example, all you'd need is the private RSA key 0.

## The IMAGE_KEY entry
![Diagram illustrating how the EKPFS is encrypted with the "mount-image" RSA key and stored in the IMAGE_KEY entry which is then encrypted with dk3.](https://i.imgur.com/Y27og84.png)

The EKPFS (dk1) is RSA encrypted with the "mount-image" public key and stored in IMAGE_KEY. We don't have the private "mount-image" RSA key, which is why for FAKE PKGs we actually replace it with flatz's generated mount-image key for Fake PKGs. This allows us to decrypt FAKE PKGs without a passcode or license, the same way flatz illustrated in his Fake PKG kernel patches in the write-up.

## Ok, whatever, but just tell me how do I decrypt some PKG I have?
So, if you want to decrypt the PFS image of any PKG, only **one** of the following items is **required**:

1. RSA key 0 (public modulus starts `d6 aa 0c 5c`)
2. RSA key 1 (public modulus starts `b9 69 53 ee`)
3. The mount-image RSA key
4. The passcode
5. The EKPFS
6. The XTS data and tweak keys

Having any of the items 1-3 would allow you to decrypt the PFS of **any** PKG. Having any of 4-6 would allow you to decrypt a **specific** PKG.

For Fake PKGs, we have replaced item 3 with our own key so we can already decrypt any Fake PKG using PkgEditor or PkgTool.

# PKG Authentication
PKG files utilize SHA-256, HMAC-SHA256, and RSA to authenticate and prevent tampering.