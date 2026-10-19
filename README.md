# BrainBreakers

[English](README.en.md) · [Español](README.es.md)

**Changer une mémoire, rejouer la recherche et montrer exactement ce qui reste faux — puis réduire le cas.**

Supprimer une source, corriger un fait et isoler deux espaces doivent changer ce qu’un système peut retrouver. Une réponse correcte ne suffit pas : elle peut cacher une source supprimée encore présente dans l’index. À l’inverse, retirer une source ne doit pas invalider une réponse encore soutenue par une source indépendante.

## Essayer

Python 3.11+ ; aucun modèle, clé ou téléchargement d’embeddings.

```sh
git clone https://github.com/gbesse/brain-breakers
cd brain-breakers
python3 -m brain_breakers serve --lang fr
```

Ouvrir `http://127.0.0.1:8772/?lang=fr`. La page affiche une **preuve enregistrée sur trois moteurs**, avec versions, résultats et cas réduits. Le bouton SQLite exécute de nouveaux essais locaux ; il ne réaffiche pas simplement le fichier enregistré. L’export JSON contient les traces et les cas minimisés exécutables.

```sh
python3 -m brain_breakers demo > preuve-sqlite.json
pip install '.[engines]'
python3 -m brain_breakers suite --backends sqlite_fts5,chroma,qdrant_local > preuve-trois-moteurs.json
python3 -m brain_breakers trial cas.json
python3 -m brain_breakers minimize cas.json
```

`pip install .` fournit aussi `brain-breakers`. UI et erreurs FR/EN/ES. Les identifiants et valeurs des cas restent des données synthétiques inchangées.

![Cas de fuite](docs/preview-fr.png)

## Quatre cas, trois moteurs réels

| Cas               | Contrôle défectueux injecté                                      | Intégration corrigée                                         |
| ----------------- | ---------------------------------------------------------------- | ------------------------------------------------------------ |
| Source supprimée  | Le client oublie de supprimer l’entrée de l’index                | Aucune source, réponse inconnue                              |
| Correction        | Le client oublie de mettre à jour une entrée existante           | `30 days` devient `14 days`, même identifiant                |
| Isolation         | Le client omet le filtre d’espace                                | Le canari de l’autre espace reste inaccessible               |
| Preuve redondante | La source supprimée reste retrouvée malgré une réponse inchangée | Même réponse, mais uniquement une source indépendante valide |

La matrice publiée exécute **12 paires défectueux/corrigé, soit 24 essais**, plus les rejeux du réducteur : 12 fautes détectées et 12 intégrations corrigées conformes. SQLite FTS5 **3.40.1**, Chroma **1.5.9**, Qdrant client local **1.19.1**. Ces numéros sont les versions de l’essai enregistré ; la CI peut avoir un SQLite différent. Les quatre cas passent aussi les tests sur les trois moteurs en CI.

**Les fautes sont créées dans notre couche client. Nous n’avons découvert ni reproduit douze bugs de Chroma, Qdrant ou SQLite.** Les opérations réelles `upsert`, `delete` et recherche filtrée sont exécutées dans chaque moteur. Chroma et Qdrant reçoivent des vecteurs déterministes par hachage des mots, sans modèle ni comparaison de pertinence sémantique. Chroma a sa télémétrie anonymisée désactivée ; Qdrant utilise `:memory:`.

## Oracle et réduction

Un registre source indépendant applique chaque mutation. L’oracle sélectionne le fait de révision déclarée la plus élevée dans l’espace demandé ; des faits contradictoires également actuels imposent l’abstention. Le test compare réponse, révision exacte, sources retrouvées et isolation — pas seulement les sources citées. Un canari remonté est un échec même si le texte final paraît correct.

Le réducteur retire les documents de bruit, rejoue le vrai moteur et conserve **succès initial + même signature d’échec après mutation**. Les documents ciblés par les mutations restent protégés. Il répète les suppressions jusqu’à un point fixe ; minimalité locale pour une suppression de document non protégé, pas minimum global du texte ou de toutes les opérations.

Les cas JSON sont bornés à 24 documents et 12 opérations. `brain_breakers.adapters` expose le contrat `upsert(document)`, `delete(id)`, `retrieve(query, scope=True)`, `close()` et `version`. Ajouter sa classe à `ADAPTERS` permet de rejouer les mêmes essais sur un autre moteur ; les adaptateurs fournis utilisent réellement les API de base de données. Aucun adaptateur GBrain/Hindsight n’est inclus ou validé.

## Existant et limites

[brain-ci](https://github.com/gbesse/brain-ci) compare déjà des contrats de connaissance entre révisions. [GBrain Evals](https://github.com/garrytan/gbrain-evals) et [tbench](https://github.com/compresh/tbench) proposent déjà des diagnostics de mémoire. Ce projet cible une preuve courte **mutation → documents effectivement retrouvés → défaut d’intégration → cas réduit → réparation**, pas un nouveau classement général.

Les API de [mise à jour Chroma](https://docs.trychroma.com/docs/collections/update-data) et [suppression Chroma](https://docs.trychroma.com/docs/collections/delete-data) servent de contrats d’intégration. L’[incident Hindsight #3912](https://github.com/vectorize-io/hindsight/issues/3912) concerne une autre défaillance de consolidation : il a motivé la recherche, mais **n’est pas reproduit par cette matrice**.

Les valeurs sont des faits structurés déclarés, pas des réponses naturelles d’un agent. Pas de preuve de causalité sur un LLM, de qualité de récupération générale, de suppression physique des sauvegardes, de conformité juridique à l’effacement, de panne disque ou de fonctionnement distribué. Le scénario de canari est synthétique. Aucun usage humain ou avantage SOTA n’est déduit de ces essais.

## Vérifier

```sh
pip install '.[engines]'
python3 -m unittest discover -s tests -v
npm ci
npx playwright install chromium
npm run test:browser
npm run format:check
```

Douze tests, dont les matrices Chroma et Qdrant ; si leurs dépendances optionnelles sont absentes, ces deux tests sont explicitement ignorés. La CI installe les deux et ne les ignore pas. Navigateur FR/EN/ES : preuve enregistrée, rejeu SQLite, filtres, redondance, export et mobile. CI Python 3.11/3.12, construction et roue hors sources. Licence MIT ; alpha publique.
