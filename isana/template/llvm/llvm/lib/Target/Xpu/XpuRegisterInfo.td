//=== Registers
class {{ namespace }}Reg<bits<6> Enc, string n, list<string> alt = []>: Register<n> {
    let HWEncoding{5-0} = Enc;
    let AltNames = alt;
    let Namespace = "{{ namespace }}";
}

{% for reg in reg_defs -%}
def {{ reg.varname }} : {{ namespace }}Reg<{{ reg.no }}, "{{ reg.name }}", {{ reg.aliases }}>, DwarfRegNum<[{{ reg.dwarfno }}]>;
{% endfor %}

//=== Register Classes
{% for regcls in regcls_defs -%}
def {{ regcls.varname }} : RegisterClass<"{{ namespace }}", [i32], 32, (add
  {{ regcls.reg_varnames }}
)>;
{% endfor %}
