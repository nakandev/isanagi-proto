//=== Registers
{% for base in reg_bases -%}
class {{ Xpu }}{{ base.name }}<bits<{{ base.bitsize }}> Enc, string n, list<string> alt = []>: Register<n> {
    let HWEncoding{ {{ base.bitsize - 1 }}-0} = Enc;
    let AltNames = alt;
    let Namespace = "{{ Xpu }}";
}
{% endfor %}

let FallbackRegAltNameIndex = NoRegAltName in
def ABIRegAltName : RegAltNameIndex;

{% for reg in reg_defs -%}
def {{ reg.varname }} : {{ Xpu }}{{ reg.basename }}<{{ reg.no }}, "{{ reg.name }}", {{ reg.aliases }}>, DwarfRegNum<[{{ reg.dwarfno }}]>{% if reg.has_aliases %}{ let RegAltNameIndices = [ABIRegAltName]; }{% else %};{% endif %}
{% endfor %}

//=== Register Classes
{% for regcls in regcls_defs -%}
def {{ regcls.varname }} : RegisterClass<"{{ Xpu }}", [i32], 32, (add
  {{ regcls.reg_varnames }}
)>;
{% endfor %}
