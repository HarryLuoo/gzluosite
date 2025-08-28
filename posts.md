---
layout: page
title: Posts
permalink: /posts/
---

<ul>
  {% for post in site.posts %}
    <li>
      <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
      <p><strong>{{ post.date | date: "%B %d, %Y" }}</strong></p>
      {% if post.description %}
        <p>{{ post.description }}</p>
      {% else %}
        <p>{{ post.content | strip_html | truncatewords: 20 }}</p>
      {% endif %}
    </li>
  {% endfor %}
</ul>
