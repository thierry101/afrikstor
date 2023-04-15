import json
import os
import random
import itertools
import string
from django.conf import settings
import re
import base64
from django.core.files.base import ContentFile
from mimetypes import guess_extension, guess_type


# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
# MAX_UPLOAD_SIZE = "2621440"
regex = '^[a-z0-9]+[._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
phoneReg = '^(2|6)[0-9]{8}$'
anyPhoneNumber = '^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$'
charReg = '^[a-zA-Z]+[\D]+?$'
# passwordReg = '^(?=(.*[0-9]))(?=.*[a-z])(?=(.*[A-Z]))(?=(.*)).{5,}$'
passwordReg = '^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{8,}$'
priceReg = '^[+]?([1-9]\d*(\.\d*[1-9])?|0\.\d*[1-9]+)|\d+(\.\d*[1-9])?$'
intCheck = '^[0-9]*$'


# *************** check length of sentence **********************************
def checkLenOfField(key, sentence, length, errors):
    if (sentence and len(str(sentence)) == 0) or sentence == None or sentence == '':
        errors[key] = "Ce champ est réquis"
    elif len(sentence) < length:
        errors[key] = f"ce champ doit contenir au moins {length} caractères"
    else:
        return sentence

# *************** check update of sentence **********************************


def checkUpdateField(sentence):
    if (sentence and len(str(sentence)) == 0) or sentence == None or sentence == '':
        pass
    else:
        return sentence


def checkPayment(key, field, errors):
    if field == 'undefined' or field == None or field == '':
        errors[key] = 'Veuillez choisir une méthode de paiement'
    else:
        return field

# ************************** CHECK COMPLEXITY PASSWORD ************************


def checkPassword(password1):
    if re.search(passwordReg, password1):
        return True
    return False


def setPasswordError(key, key2, password1, password2, length, errors):
    if password1:
        if checkPassword(password1) == False or len(password1) < 8:
            errors[key] = f"Votre mot de passe doit contenir au moins {length} caractères contenant une majuscule et un chiffre au moins"
        elif password1 != password2:
            errors[key2] = "Les mots de passes sont différents"
        else:
            return password1
    else:
        errors[key] = "Ce champ est requis"

# *************************** CHECK UPDATE PASSWORD ***************************


def updatePassword(request, key, key2, oldPassword, password1, password2, length, oldKey, errors):
    if oldPassword:
        checkPass = request.user.check_password(oldPassword)
        if checkPass:
            if password1:
                if checkPassword(password1) == False and len(password1) < 8:
                    errors[key] = f"Votre mot de passe doit contenir au moins {length} caractères contenant une majuscule et un chiffre au moins"
                elif password1 != password2:
                    errors[key2] = "Les mots de passes sont différents"
                else:
                    return password1
            else:
                errors[key] = "Ce champ est requis"
        else:
            errors[oldKey] = 'Ancien mot de passe incorrect'
    elif not oldPassword and password1:
        errors[oldKey] = 'Veuillez renseigner votre mot de passe'


# ********************** CHECK EMAIL ADDRESS ********************************
def checkMail(email):
    if re.search(regex, email):
        return True
    return False


def setEmailError(key, field, errors):
    if field:
        if checkMail(field) == False:
            errors[key] = "Adresse Email invalide"
        else:
            return field
    else:
        errors[key] = "Ce champ est requis"

# ************************** CHECK UPDATE EMAIL *************************************


def updateEmailField(key, field, errors):
    if field == '' or field == None:
        pass
    else:
        if checkMail(field) == False:
            errors[key] = "Adresse Email invalide"
        else:
            return field

# ////////////////////////////////////////////////////// begin of image /////////////////////////////////
# ******************************* CHECK EXTENSION OF IMAGE ****************************


def checkExtensionImg(key, field, name, file, errors):
    extensions = ['jpg', 'jpeg', 'png', 'gif']
    if field == None or field[name] == '':
        errors[key] = "Veuillez sélectionner une image"
    elif field[name] and field[file]:
        format, imgstr = field[file].split(';base64,')
        extension = format.split('/')[-1]
        if not extension in extensions:
            errors[key] = 'Veuillez choisir une image au format jpg, jpeg, png'
        else:
            return field[name]


# ******************************** CHECK EXTENSION IMAGE WHEN UPDATE ********************
def checkExtensionImgUpdate(key, field, name, file, instance, errors):
    extensions = ['jpg', 'jpeg', 'png', 'gif']
    if field and field[name] and field[file]:
        format, imgstr = field[file].split(';base64,')
        extension = format.split('/')[-1]
        if not extension in extensions:
            errors[key] = 'Veuillez choisir une image au format jpg, jpeg, png'
        else:
            mainImg = "/" + str(instance)
            if(mainImg == '/'):
                pass
            else:
                if os.path.exists(settings.MEDIA_ROOT + mainImg):
                    os.remove(settings.MEDIA_ROOT + mainImg)
                    return field[name]
                return field[name]
    else:
        pass


# *********************************** CHECK EXTENSION OF TABLE IMG ************************************
def checkExtensionOfManyImg(key, tableImg, errors):
    extensions = ['jpg', 'jpeg', 'png']
    if len(tableImg) == 0:
        errors[key] = "Veuillez sélectionner plus d'images pour cet article"
    else:
        for img in tableImg:
            fmt, imgstr = img['file'].split(';base64,')
            ext = fmt.split('/')[-1]
            if not ext in extensions:
                errors[key] = "Vos images doivent être au format jpg, jpeg, png"
            else:
                pass
        if len(errors) == 0:
            return tableImg


# *********************************** CHECK EXTENSION OF TABLE IMG ************************************
def checkExtensionUpdateManyImg(key, file, oldTableImg, tableImg, tablebase64, newTable, errors):
    extensions = ['jpg', 'jpeg', 'png']
    if len(tableImg) == 0:
        errors[key] = "Veuillez sélectionner plus d'images pour cet article"
    else:
        for img, imgs in itertools.zip_longest(tableImg, oldTableImg, fillvalue={'file': ''}):
            if 'data:image/' in img[file]:
                fmt, imgstr = img[file].split(';base64,')
                ext = fmt.split('/')[-1]
                if not ext in extensions:
                    errors[key] = "Vos images doivent être au format jpg, jpeg, png"
                else:
                    if img[file] == imgs[file]:
                        pass
                    else:
                        imagPathToDelete = settings.MEDIA_ROOT + \
                            '/' + imgs[file].split('/media/')[1]
                        if os.path.exists(imagPathToDelete):
                            os.remove(imagPathToDelete)
                    tablebase64.append(img[file])
            else:
                if img[file] == imgs[file]:
                    newTable.append({file: img[file]})
                else:
                    imagPathToDelete = settings.MEDIA_ROOT + \
                        '/' + imgs[file].split('/media/')[1]
                    if os.path.exists(imagPathToDelete):
                        os.remove(imagPathToDelete)
                    else:
                        pass
        return {"base64": tablebase64, 'pathImg': newTable}


# ****************************************** check extension of color img **************************
def checkExtensionUpdateColorImg(key, file, color, code, oldTableImg, tableImg, tableBase64, newTable, errors):
    extensions = ['jpg', 'jpeg', 'png']
    if len(tableImg) == 0:
        pass
    else:
        for img, imgs in itertools.zip_longest(tableImg, oldTableImg, fillvalue={'name': '', 'hex': '', 'img': ''}):
            if 'data:image/' in img[file]:
                fmt, imgstr = img[file].split(';base64,')
                ext = fmt.split('/')[-1]
                if not ext in extensions:
                    errors[key] = "Vos images doivent être au format jpg, jpeg, png"
                else:
                    if img[file] == imgs[file]:
                        pass
                    else:
                        tableBase64.append(img)
                        if len(imgs[file]) > 0:
                            imagPathToDelete = settings.MEDIA_ROOT + \
                                '/' + imgs[file].split('/media/')[1]
                            if os.path.exists(imagPathToDelete):
                                os.remove(imagPathToDelete)
                        else:
                            pass
            else:
                if img[file] == imgs[file]:
                    newTable.append(
                        {color: img[color], code: img[code], file: img[file]})
                else:
                    if len(imgs[file]) > 0:
                        imagPathToDelete = settings.MEDIA_ROOT + \
                            '/' + imgs[file].split('/media/')[1]
                        if os.path.exists(imagPathToDelete):
                            os.remove(imagPathToDelete)
                        else:
                            pass
                    else:
                        pass
        return {"base64": tableBase64, 'pathImg': newTable}


# **************************** CHECK EXTENSION OF TABLE COLOR IMG **********************************
def checkExtensionOfColorImg(key, tableImg, errors):
    extensions = ['jpg', 'jpeg', 'png']
    if len(tableImg) == 0:
        pass
    else:
        for img in tableImg:
            fmt, imgstr = img['img'].split(';base64,')
            ext = fmt.split('/')[-1]
            if not ext in extensions:
                errors[key] = "Vos images doivent être au format jpg, jpeg, png"
            else:
                pass
        if len(errors) == 0:
            return tableImg
        else:
            pass


# ************************************ delete image from table image ********************************
def deletePathManyImg(instance, key):
    if instance != None or instance != '':
        images = json.loads(instance)
        for img in images:
            imagPath = settings.MEDIA_ROOT + '/' + img[key].split('/media/')[1]
            if os.path.exists(imagPath):
                os.remove(imagPath)
    else:
        pass


# *************************************** delete single image ************************************
def deleteOneImg(instance):
    mainImg = "/" + str(instance)
    if(mainImg == '/'):
        pass
    else:
        if os.path.exists(settings.MEDIA_ROOT + mainImg):
            os.remove(settings.MEDIA_ROOT + mainImg)
        else:
            pass
# ////////////////////////////////////////////////////// end of image /////////////////////////////////


# **************************** GERATOR OF RANDOM VALUE ***********************************
def id_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for x in range(size))


# **************************** GERATOR OF RANDOM order number ***********************************
def gererateOrderNber(code, size=5, chars=string.ascii_uppercase + string.digits):
    return code + "".join(random.choice(chars) for x in range(size))


# **************************** GERATOR OF RANDOM order number ***********************************
def generateNumber(code, size=5, chars=string.digits):
    return code + "".join(random.choice(chars) for x in range(size))


# ************************** CHECK IF ID IS SELECTED **************************************
def checkIdSelected(key, field, name, errors):
    if field == '' or field == None:
        errors[key] = f"Veuillez choisir {name}"
    else:
        return int(field)


# ****************************** CHECK VALUE OF STATUT *************************************
def checkStatus(field):
    if field == None:
        return True
    else:
        return field


# *********************************** CHECK IF ITEM IS UNIQUE ******************************
def checkUniqueItem(key, table, field, errors):
    instance = table.objects.filter(name=(str(field))).first()
    if instance != None and instance.name == field:
        errors[key] = "Cette valeur existe déjà"
    elif instance == None:
        return field


# ****************************** CHECK UNIQUE USER ******************************************
def checkUniqueUser(key, table,  email, errors):
    instance = table.objects.filter(email=email).first()
    if instance != None and instance.email == email:
        errors[key] = "Cette adresse email existe déjà"


# ****************************** CHECK PHONE NUMBER ******************************************
def checkPhoneNumber(field):
    if re.match(phoneReg, field):
        return True
    return False


def checkPhoneError(key, field, errors):
    if field:
        if checkPhoneNumber(field) == False:
            errors[key] = 'Numéro de téléphone invalide'
        else:
            return field
    else:
        errors[key] = 'Ce champ est requis'

# ********************************* CHECK ANY PHONE NUMBER *******************************************


def checkAnyPhoneNumber(field):
    if re.match(anyPhoneNumber, field):
        return True
    return False


def checkPhoneError(key, field, errors):
    if field:
        if checkAnyPhoneNumber(field) == False:
            errors[key] = 'Numéro de téléphone invalide'
        else:
            return field
    else:
        errors[key] = 'Ce champ est requis'


# ****************************** CHECK PHONE NUMBER WHEN UPDATE ******************************************
def updatePhone(key, field, errors):
    if field == '' or field == None:
        return None
    else:
        if checkPhoneNumber(field) == False:
            errors[key] = 'Numero de téléphone invalide'
        else:
            return field

# ************************************ NO FOR ALL PROJECT ********************************
def convToString(key, sentence, message, errors):
    if sentence and 'Choi' in sentence:
        errors[key] = f"Veuillez choisir {message}"
    else:
        if sentence:
            return int(sentence)
        else:
            pass

# ****************************** CHECK IF STRING AND CONVERT TO INTEGER ******************************************
def convertToInt(key, sentence, message, errors):
    if (isinstance(sentence, str) and len(sentence) > 1) or sentence == '':
        errors[key] = f"Veuillez choisir {message}"
    else:
        if sentence:
            return int(sentence)
        else:
            pass


# ******************************************* CHECK TABLE ID **********************************************
def checkTableId(key, table, message, errors):
    newtable = []
    if len(table) == 0:
        errors[key] = f"Veuillez choisir {message}"
    else:
        for el in table:
            if isinstance(el, str):
                errors[key] = f"Veuillez choisir {message}"
            else:
                newtable.append(el)
        return newtable


# ************************************ CHECK TABLE COLOR *****************************************************
def checkTableColor(key, table, errors):
    if len(table) == 0:
        pass
        # errors[key] = 'Veuillez choisir les couleurs'
    else:
        return table


# *************************************** CHECK TYPE OF PRICE ***********************************************
def checkPrices(key, price, errors):
    if price == '' or price == None:
        errors[key] = 'Veuillez entrez un prix'
    else:
        return float(price)


# *************************************** CHECK SOLD_PRICE ***********************************************
def checkSoldPrice(key, price, sold_price, errors):
    if price and sold_price:
        if float(sold_price) > float(price):
            errors[key] = "Le prix de solde doit être inférieur"
        else:
            return sold_price


# *************************** CHECK IF DATE ANS COMPARE *****************************************************
def checkDateAndCompare(key1, key2, date1, date2, errors):
    if date1 == '' or date1 == None:
        errors[key1] = 'Veuillez sélectionner une date'
    elif date2 == '' or date2 == None:
        errors[key2] = 'Veuillez sélectionner une date'
    else:
        if date1 and date2 and date1 > date2:
            errors[key1] = 'La date de fin doit être supérieure'
        else:
            return {'startDate': date1, 'endDate': date2}


def checkStartWith(key, value, wordStart, errors):
    if value == '' or value == None:
        errors[key] = 'Ce champ est requis'
    else:
        if value.startswith(wordStart):
            return value
        else:
            errors[key] = "Ce code n'est pas valide"


# *************************** begin of trash ********************************


def setEmailErrorNotRequire(key, field, error):
    if field:
        if checkMail(field) == False:
            error.append({key: 'Adresse Email invalide'})
        else:
            return field
    # else:
    #     error.append({key: 'Ce champ est requis'})
# ************************************ UPDATE FIELD **************************************


def updateEmail(key, field, error):
    if field == '' or field == None:
        return None
    else:
        if checkMail(field) == False:
            error.append({key: 'Adresse Email invalide'})
        else:
            return field


def updateField(key, field, lenght, error):
    if field == '' or field == None:
        return None
    else:
        if len(field) < lenght:
            error.append(
                {key: f"ce champ doit contenir au moins {lenght} caractères"})
        else:
            return field


def updateSingleImg(key, field, error):
    extensions = ['jpg', 'jpeg', 'png']
    if not 'name' in field or field['name'] == '':
        error.append({
            key: 'Votre image doit etre au format jpg, jpeg, png'
        })
    else:
        if not str(field['name']).split(".")[-1] in extensions:
            error.append({
                key: 'Votre image doit etre au format jpg, jpeg, png'
            })
        else:
            return str(field['name'])


def updateSettingImg(key, field, error):
    extensions = ['jpg', 'jpeg', 'png']
    if 'name' in field:
        if not str(field['name']).split(".")[-1] in extensions:
            error.append({
                key: 'Votre image doit etre au format jpg, jpeg, png'
            })
        else:
            return str(field['name'])


def saveUpdateLogo(name, file, instance):
    if name == None:
        pass
    else:
        logoImg = "/" + str(instance.logo)
        if not logoImg == "/":
            os.remove(settings.MEDIA_ROOT + logoImg)
        format, imgstr = file.split(';base64,')
        instance.logo = ContentFile(
            base64.b64decode(imgstr), name=str(name))
        instance.save()


def saveUpdateMainImg(name, file, instance):
    if name == None:
        pass
    else:
        mainImg = "/" + str(instance.imgHome)
        if not mainImg == "/":
            os.remove(settings.MEDIA_ROOT + mainImg)
        format, imgstr = file.split(';base64,')
        instance.imgHome = ContentFile(
            base64.b64decode(imgstr), name=str(name))
        instance.save()


# *************************** END UPDATE FIELD *************************************


def checkCharField(field, minLength):
    return (len(field) > minLength and len(field) < 255) and (re.match(charReg, field))


def setErrorKeyField(key, request, minLength, error):
    if key not in request.POST:
        error.append({key: 'Ce champ est requis'})
    else:
        if checkCharField(request.POST[key], minLength) == False:
            error.append(
                {key: f'Ce champ doit contenir au moins {minLength} caractères'})
        elif len(request.POST[key]) == 0 or request.POST[key] == 'null' or request.POST[key] == None:
            error.append({key: 'Ce champ est obligatoire'})
        else:
            return request.POST[key]


def chekKeyExists(key, request):
    # verifie si une cle existe dans une requete
    if key in request.POST:
        return request.POST[key]
    elif key in request.FILES:
        return request.FILES[key]
    else:
        pass


def setErrorField(field, fieldName, minLength, error):
    if field:
        if checkCharField(field, minLength) == False:
            error.append(
                {fieldName: f'Ce champ doit contenir au moins {minLength} caractères'})
    else:
        error.append({fieldName: 'Ce champ est requis'})


def checkKeyInData(key, data, error):
    if key in data:
        return data[key]
    else:
        error.append({key: f"Vous devez choisir un(e) {key}"})


def checkLenAndCompareNumber(key, sentence, error):
    if len(sentence) == 0 or sentence == None:
        error.append({key: "Ce champ est réquis"})
    elif int(sentence) > 5:
        error.append(
            {key: "Les notes sont comprises entre 0 et 5"})
    else:
        return sentence


def checkPrice(field):
    if re.match(priceReg, field):
        return True
    return False


def setPriceError(key, field, error):
    if field:
        if checkPrice(field) == False:
            error.append(
                {key: 'Ce champ ne doit contenir que des chiffes positifs'})
        else:
            return field


def checkPathDelete(oldPathTab, newPathTab, newTab, delTab):
    # verifie les chemins a supprimer
    for el in oldPathTab:
        if el in newPathTab:
            newTab.append(el)
        else:
            delTab.append(el)


def checkIfNumber(key, field, error):
    if field == '' or field == None:
        error.append(
            {key: "Ce champ est requis"}
        )
    elif not field.isnumeric():
        error.append(
            {key: "Vous devez entrer des chiffres"}
        )
    else:
        return field


# **************************** CHECK IF NUMBER *********************************


def checkInt(sentence):
    if re.search(intCheck, sentence):
        return True
    return False


def setIntNumberError(key, field, error):
    if checkInt(str(field)) == False:
        error[key] = "Ce champ doit contenir uniquement des chiffres"
    elif len(str(field)) > 4 or len(str(field)) < 4:
        error[key] = "Ce champ doit contenir 4 caractères"
    else:
        return field

# ***************************** CHECK EXTENSION AND SIZE FIELD *********************************


def checkExtensionAndSize(key, theRequest, max_size,  errors):
    extensions = ['pdf']
    if theRequest and key in theRequest:
        file = theRequest[key]
        name = str(file).split(".")[-1]
        if not name in extensions:
            errors[key] = 'Veuillez choisir une image au format jpg ou jpeg'
        elif round(float(file.size/1048576), 2) > max_size:
            errors[key] = f'Votre fichier ne doit pas excéder {max_size} Mb'
        else:
            return str(file)
    else:
        errors[key] = 'Veuillez sélectionner un fichier'

# **************************** CHECK EXTENSION OF IMAGE ************************************


def checkExtensionOfImg(key, field, errors):
    extensions = ['jpg', 'jpeg', 'png']
    if 'name' in field:
        if str(field['name']) == '':
            errors[key] = 'Veuillez sélectionner une image'
        elif str(field['name']) != '' and not str(field['name']).split(".")[-1] in extensions:
            errors[key] = 'Votre image doit etre au format jpg, jpeg, png'
        else:
            return str(field['name'])
    else:
        errors[key] = 'Veuillez sélectionner une image'

# ********************** CHECK EXTENSION OF A TABLE IMAGES *******************************
