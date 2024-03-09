# Documentation du code

Ce document est une documentation du code Python app.py fourni. Il décrit les fonctions et les variables utilisées dans le code ainsi que leur objectif.

## Fonctions principales

### load_doc(file_path)
Cette fonction charge un document PDF à partir du chemin spécifié et le divise en pages. Elle utilise la classe `PyPDFLoader` pour charger le document et la classe `RecursiveCharacterTextSplitter` pour diviser le texte en chunks.

### initialize_database(file_path)
Cette fonction initialise une base de données vectorielle à partir du document PDF spécifié. Elle utilise la fonction `load_doc` pour charger le document, puis crée une base de données vectorielle à l'aide de la fonction `create_db`.

### create_db(splits, collection_name)
Cette fonction crée une base de données vectorielle à partir des fragments de texte fournis et d'un nom de collection spécifié. Elle utilise la classe `HuggingFaceEmbeddings` pour obtenir des embeddings des fragments de texte et la classe `Chroma` pour créer la base de données vectorielle. Visitez https://docs.trychroma.com/ pour plus d'informations.

### initialize_llmchain(temperature, max_tokens, top_k, vector_db)
Cette fonction initialise une chaîne de traitement de modèle de langage avec un modèle Hugging Face. Elle utilise une base de données vectorielle spécifiée pour la récupération de documents et crée une chaîne de traitement de conversation à l'aide de la classe `HuggingFaceEndpoint`, cette dernière prend en arguments aussi la variable huggingfacehub_api_token qui est l'access token de HuggingFace. Pour plus de sécurité il est mieux de le définir avec les variables d'environement.

### format_chat_history(message, chat_history)
Cette fonction formate l'historique de chat sous forme de messages utilisateur et assistant, pour une meilleure lisibilité. Elle prend un message utilisateur et l'historique de chat comme entrée et retourne l'historique formaté.

### conversation(message, history)
Cette fonction représente une conversation entre un utilisateur et un assistant. Elle prend un message utilisateur et l'historique de la conversation comme entrée, formate l'historique de chat, génère une réponse en utilisant la chaîne de traitement de modèle de langage initialisée précédemment, puis retourne la réponse.

## Variables principales

- `splt`: Variable contenant les fragments de texte extraits du document PDF.
- `vec`: Variable contenant la base de données vectorielle initialisée à partir du document PDF.
- `vec_cre`: Variable contenant une autre instance de la base de données vectorielle initialisée.
- `qa`: Variable contenant la chaîne de traitement de modèle de langage initialisée.

Voici une section que vous pourriez ajouter à votre fichier README.md pour documenter le fine-tuning du modèle :


## Fine-tuning du modèle

Le processus de fine-tuning, ou affinage en français, permet d'adapter un modèle de langage pré-entraîné à des tâches spécifiques ou à des jeux de données personnalisés. Dans le cadre de ce projet, vous pouvez effectuer le fine-tuning du modèle de la manière suivante :

### Entraînement sur différents modèles

Le paramètre `repo_id` dans la fonction `initialize_llmchain` permet de spécifier le modèle Hugging Face à utiliser pour le fine-tuning. Vous pouvez remplacer la valeur actuelle (`mistralai/Mixtral-8x7B-Instruct-v0.1`) par l'identifiant d'un autre modèle disponible sur la plateforme Hugging Face. Cela vous permet d'explorer différents modèles pour trouver celui qui convient le mieux à votre tâche spécifique.
Ce modèle était adéquat tant qu'il comprend 5 languages différentes.

### Entraînement sur des données personnalisées

Outre l'utilisation de modèles pré-entraînés, vous pouvez également entraîner le modèle sur des données personnalisées. Par exemple, vous pouvez fournir des documents PDF contenant des données spécifiques à votre domaine d'application pour améliorer les performances du modèle sur des tâches spécifiques. Ici le site data.gov.ma utilisé comme contexte.

### Modification des hyperparamètres

La fonction `initialize_llmchain` permet également de modifier les hyperparamètres du modèle, tels que la température, le nombre maximal de jetons générés (`max_tokens`), et le paramètre `top_k`. Vous pouvez ajuster ces hyperparamètres en fonction des besoins de votre tâche spécifique, afin d'optimiser les performances du modèle.

Voici une section d'utilisation que vous pouvez ajouter à votre fichier README.md :


## Utilisation

La fonction `conversation` est utilisée pour obtenir une réponse à une question posée dans le contexte du PDF. Voici comment utiliser cette fonction :

1. **Questionnement dans le contexte du PDF :** Vous pouvez poser une question en rapport avec le contenu du PDF. La fonction `conversation` prend en entrée le message de l'utilisateur et l'historique de la conversation, et retourne la réponse générée par le modèle.

2. **Déploiement avec Gradio :** Vous pouvez déployer l'interface de conversation à l'aide de Gradio, que ce soit en ligne avec Hugging Face ou localement. Voici comment :

    - **Déploiement en ligne avec Hugging Face :** L'interface de conversation peut être déployée en ligne en utilisant les services de déploiement de modèles de Hugging Face. Cela permet aux utilisateurs d'interagir avec le modèle via une interface conviviale directement depuis leur navigateur.

    - **Déploiement local avec Gradio :** Si vous préférez, vous pouvez également déployer l'interface localement en utilisant la fonction `gr.ChatInterface(conversation).launch()`. Cela lance une interface de conversation dans votre environnement local, où vous pouvez poser des questions et obtenir des réponses en temps réel.


## Déploiement

Vous pouvez essayer une démo du chatbot en ligne en accédant au lien suivant : [Démo du Chatbot](https://huggingface.co/spaces/skalilopa/data_gov_ma). Cette démo vous permettra d'interagir avec le chatbot et de poser des questions dans le contexte du PDF.

## API

Pour utiliser l'API du chatbot avec Python, vous pouvez suivre les étapes suivantes :

```python
$ pip install gradio_client
from gradio_client import Client

client = Client("tferhan/data_gov_ma")
result = client.predict(
		"Hello!!",	# Message à envoyer
		api_name="/chat"
)
print(result)
```

Et voici comment le faire en JavaScript :

```javascript
$ npm i -D @gradio/client
import { client } from "@gradio/client";

const app = await client("tferhan/data_gov_ma");
const result = await app.predict("/chat", [		
				"Hello!!", // Message à envoyer
	]);

console.log(result.data);
```

