//=== Registers
{% for base in reg_bases -%}
class {{ namespace }}{{ base.name }}<bits<{{ base.bitsize }}> Enc, string n, list<string> alt = []>: Register<n> {
    let HWEncoding{ {{ base.bitsize - 1 }}-0} = Enc;
    let AltNames = alt;
    let Namespace = "{{ namespace }}";
}
{% endfor %}

{% for reg in reg_defs -%}
def {{ reg.varname }} : {{ namespace }}{{ reg.basename }}<{{ reg.no }}, "{{ reg.name }}", {{ reg.aliases }}>, DwarfRegNum<[{{ reg.dwarfno }}]>;
{% endfor %}

//=== Register Classes
{% for regcls in regcls_defs -%}
def {{ regcls.varname }} : RegisterClass<"{{ namespace }}", [i32], 32, (add
  {{ regcls.reg_varnames }}
)>;
{% endfor %}
