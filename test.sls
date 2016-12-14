aa:
   cmd.run:
{% if grains['fqdn'].split('-')[0] == 'hd1' %}
      - name: echo -e "aaa bbb" >> /etc/hosts
{% else %}
      - name: echo -e "aaa bbb" >> /etc/hosts
{%endif%}
