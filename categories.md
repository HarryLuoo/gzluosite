---
layout: page
title: Categories
permalink: /categories/
---

<div>
  {% for category in site.categories %}
    <h2 id="{{ category[0] | slugify }}">{{ category[0] }}</h2>
    <ul>
      {% for post in category[1] %}
        <li>
          <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
          <span style="font-size: 0.8em; color: #666;"> - {{ post.date | date: "%B %d, %Y" }}</span>
        </li>
      {% endfor %}
    </ul>
  {% endfor %}
</div>
