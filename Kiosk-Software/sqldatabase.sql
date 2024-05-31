CREATE DATABASE IF NOT EXISTS newlanguage_db;

USE newlanguage_db;

CREATE TABLE IF NOT EXISTS TranslationsTable (
    id INT PRIMARY KEY AUTO_INCREMENT,
    keyword VARCHAR(50) NOT NULL,
    marathi_translation VARCHAR(100),
    hindi_translation VARCHAR(100),
    english_translation VARCHAR(100),
    tamil_translation VARCHAR(100),
    french_translation VARCHAR(100),
    german_translation VARCHAR(100)
);

INSERT INTO TranslationsTable (keyword, marathi_translation, hindi_translation, english_translation, tamil_translation, french_translation, german_translation)
VALUES
    ('Emergency', 'आपत्ती', 'आपातकालीन', 'Emergency', 'அவசரம்', 'Urgence', 'Notfall'),
    ('FAQ', 'सामान्य प्रश्नांची अचूक माहिती', 'सामान्य प्रश्न', 'Frequently Asked Questions', 'அனைத்து கேள்விகளுக்கும் பதில்', 'Foire Aux Questions', 'Häufig gestellte Fragen'),
    ('Select option from below', 'कृपया खालीलमधून निवडा', 'कृपया खालीलमधून निवडा', 'Select option from below', 'கீழுள்ளிருந்து ஒரு விருப்பத்தை தேர்ந்தெடு', 'Sélectionnez une option ci-dessous', 'Option auswählen'),
    ('PNR', 'पीएनआर', 'पीएनआर', 'PNR', 'பி.என்.ஆர்', 'PNR', 'PNR'),
    ('Recent Announcement', 'आजचे घोषणा', 'हालचाल की घोषणा', 'Recent Announcement', 'சமீபத்திய அறிவிப்பு', 'Annonce récente', 'Aktuelle Ankündigung'),
    ('Helpline', 'सहाय्यसूची', 'हेल्पलाईन', 'Helpline', 'உதவிக் கோருகை', 'Ligne d''assistance', 'Hotlinenummer'),
    ('Station Information', 'स्थानक माहिती', 'स्थानीय जानकारी', 'Station Information', 'நிலைய தகவல்', 'Information sur la station', 'Bahnhofsinformation'),
    ('PNR Status Checker', 'पीएनआर स्थिती तपासकर्ता', 'PNR स्थिति चेकर', 'PNR Status Checker', 'பி.என்.ஆர் நிலை சரிபார்க்குனர்', 'Vérificateur de statut PNR', 'PNR-Status-Überprüfer'),
    ('Home', 'मुख्यपृष्ठ', 'होम', 'Home', 'வீடு', 'Accueil', 'Zuhause'),
    ('Enter PNR Number', 'पीएनआर नंबर प्रविष्ट करा', 'PNR नंबर दर्ज करें', 'Enter PNR Number', 'பி.என்.ஆர் எண் உள்ளிடவும்', 'Entrer le numéro PNR', 'PNR-Nummer eingeben');

UPDATE TranslationsTable
SET
    marathi_translation = 'नवीन मराठी भाषांतर',
    hindi_translation = 'नया हिंदी अनुवाद',
    english_translation = 'New English Translation',
    tamil_translation = 'புதிய தமிழ் மொழிபெயர்ப்பு',
    french_translation = 'Nouvelle traduction en français',
    german_translation = 'Neue deutsche Übersetzung'
WHERE keyword IN ('Home', 'Enter PNR Number');

SELECT * FROM TranslationsTable;
