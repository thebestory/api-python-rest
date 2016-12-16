# Заметки
Место для заметок

## Мысли

* История и комментарий сами по себе являются очень похожими объектами как по модели, так и по внешнему "виду". Интересно, стоит создать одну общую модель для них, или оставить их раздельными...

## Роуты

#### Users

* Get user
  * **GET** _/users/**{user.username}**_
  * Type: User, 200 OK

* Get current user
  * **GET** _/users/**{@me}**_
  * Type: User, 200 OK

* Modify current user
  * **PATCH** _/users/**{@me}**_
  * Type: User, 200 OK
  * Params:
    * username (string)
    * avatar (bytes) - multipart must be used

#### Topics

* Get list of topics
  * **GET** _/topics_
  * Type: list\[Topic\], 200 OK

* Get topic
  * **GET** _/topics/**{topic.slug}**_
  * Type: Topic, 200 OK

* Get latest stories in topic
  * **GET** _/topics/**{topic.slug}**/latest_
  * Type: list\[Story\], 200 OK

* Get hot stories in topic
  * **GET** _/topics/**{topic.slug}**/hot_
  * Type: list\[Story\], 200 OK

* Get top stories in topic
  * **GET** _/topics/**{topic.slug}**/top_
  * Type: list\[Story\], 200 OK

* Get random stories in topic
  * **GET** _/topics/**{topic.slug}**/random_
  * Type: list\[Story\], 200 OK

#### Stories

* Get story
  * **GET** _/stories/**{story.id}**_
  * Type: Story, 200 OK

* Submit story
  * **POST** _/stories_
  * Type: Story, 201 Created
  * Params:
    * content (string), max length: 4000 symbols

* Edit story
  * **PATCH** _/stories/**{story.id}**_
  * Type: Story, 200 OK
  * Params:
    * content (string), max length: 4000 symbols
    * is_approved (bool)

* Delete story
  * **DELETE** _/stories/**{story.id}**_
  * Type: 204 No content

* Story comments
  * **GET** _/stories/**{story.id}**/comments_
  * Type: list\[Comment\], 200 OK

#### Comments

* Get comment
  * **GET** _/comments/**{comment.id}**_
  * Type: Comment, 200 OK

* Edit comment
  * **PATCH** _/comments/**{comment.id}**_
  * Type: Comment, 200 OK
  * Params:
    * content (string), max length: 2000 symbols

* Delete comment
  * **DELETE** _/comments/**{story.id}**_
  * Type: 204 No content

* Comment replies
  * **GET** _/stories/**{story.id}**/replies_
  * Type: list\[Comment\], 200 OK

* Submit reply
  * **POST** _/comments/**{comment.id}**/replies_
  * Type: Comment, 201 Created
  * Params:
    * content (string), max length: 2000 symbols
