import re
from aida_tools.descriptors import TextDescriptor
from vistautils.span import Span
from aida_tools.corpus import TextJustificationLookup


def parse_text_from_source(text_justification_lookup: TextJustificationLookup,
                           inf_just_pattern,
                           inf_just_span):
    match = re.search(inf_just_pattern, inf_just_span)
    if match:
        # source = match.group(1)
        document = match.group(2)
        start = int(match.group(3))
        end = int(match.group(4))
        text_descriptor = TextDescriptor(doceid=document,
                                         span=Span.from_inclusive_to_exclusive(start, end + 1),
                                         language=None)
        try:
            lookup = text_justification_lookup.text_for_justification(text_descriptor, 50)
            return lookup.spanning_tokens, lookup.original_text
        except (RuntimeError, AttributeError):
            return 'None', 'None'
    else:
        return 'None', 'None'
