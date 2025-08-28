---
layout: page
title: Tags
permalink: /tags/
---

<div class="tags-archive">
  {% for tag in site.tags %}
    <h2 id="{{ tag[0] | slugify }}">{{ tag[0] }}</h2>
    <ul>
      {% for post in tag[1] %}
        <li>
          <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
          <span style="font-size: 0.8em; color: #666;"> - {{ post.date | date: "%B %d, %Y" }}</span>
        </li>
      {% endfor %}
    </ul>
  {% endfor %}
</div>
