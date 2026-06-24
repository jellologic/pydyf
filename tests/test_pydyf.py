import io
import re

import pytest

import pydyf

from . import assert_pixels


@pytest.mark.parametrize('compress', [False, True])
def test_fill(compress):
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(2, 2, 5, 6)
    draw.fill()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __________
        __________
    ''', compress)


def test_stroke():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(2, 2, 5, 6)
    draw.set_line_width(2)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        _KKKKKKK__
        _KKKKKKK__
        _KK___KK__
        _KK___KK__
        _KK___KK__
        _KK___KK__
        _KKKKKKK__
        _KKKKKKK__
        __________
    ''')


def test_line_to():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.move_to(2, 2)
    draw.set_line_width(2)
    draw.line_to(2, 5)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __________
        __________
        __________
        _KK_______
        _KK_______
        _KK_______
        __________
        __________
    ''')


def test_set_color_rgb_stroke():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(2, 2, 5, 6)
    draw.set_line_width(2)
    draw.set_color_rgb(0, 0, 255, stroke=True)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        _BBBBBBB__
        _BBBBBBB__
        _BB___BB__
        _BB___BB__
        _BB___BB__
        _BB___BB__
        _BBBBBBB__
        _BBBBBBB__
        __________
    ''')


def test_set_color_rgb_fill():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(2, 2, 5, 6)
    draw.set_color_rgb(255, 0, 0)
    draw.fill()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __RRRRR___
        __RRRRR___
        __RRRRR___
        __RRRRR___
        __RRRRR___
        __RRRRR___
        __________
        __________
    ''')


def test_set_dash():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.move_to(2, 2)
    draw.set_line_width(2)
    draw.line_to(2, 6)
    draw.set_dash([2, 1], 0)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __________
        __________
        _KK_______
        __________
        _KK_______
        _KK_______
        __________
        __________
    ''')


def test_curve_to():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.move_to(2, 5)
    draw.set_line_width(2)
    draw.curve_to(2, 5, 3, 5, 5, 5)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __________
        __________
        __KKK_____
        __KKK_____
        __________
        __________
        __________
        __________
    ''')


def test_curve_start_to():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.move_to(2, 5)
    draw.set_line_width(2)
    draw.curve_start_to(3, 5, 5, 5)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __________
        __________
        __KKK_____
        __KKK_____
        __________
        __________
        __________
        __________
    ''')


def test_curve_end_to():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.move_to(2, 5)
    draw.set_line_width(2)
    draw.curve_end_to(3, 5, 5, 5)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __________
        __________
        __KKK_____
        __KKK_____
        __________
        __________
        __________
        __________
    ''')


def test_set_matrix():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.set_matrix(1, 0, 0, 1, 1, 1)
    draw.move_to(2, 2)
    draw.set_line_width(2)
    draw.line_to(2, 5)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __________
        __________
        __KK______
        __KK______
        __KK______
        __________
        __________
        __________
    ''')


def test_set_state():
    document = pydyf.PDF()

    graphic_state = pydyf.Dictionary({
        'Type': '/ExtGState',
        'LW': 2,
    })
    document.add_object(graphic_state)

    draw = pydyf.Stream()
    draw.rectangle(2, 2, 5, 6)
    draw.set_state('GS')
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
        'Resources': pydyf.Dictionary({
            'ExtGState': pydyf.Dictionary({'GS': graphic_state.reference}),
        }),
    }))

    assert_pixels(document, '''
        __________
        _KKKKKKK__
        _KKKKKKK__
        _KK___KK__
        _KK___KK__
        _KK___KK__
        _KK___KK__
        _KKKKKKK__
        _KKKKKKK__
        __________
    ''')


def test_fill_and_stroke():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(2, 2, 5, 6)
    draw.set_line_width(2)
    draw.set_color_rgb(0, 0, 255, stroke=True)
    draw.fill_and_stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        _BBBBBBB__
        _BBBBBBB__
        _BBKKKBB__
        _BBKKKBB__
        _BBKKKBB__
        _BBKKKBB__
        _BBBBBBB__
        _BBBBBBB__
        __________
    ''')


def test_clip():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(3, 3, 5, 6)
    draw.rectangle(4, 3, 2, 6)
    draw.clip()
    draw.end()
    draw.move_to(0, 5)
    draw.line_to(10, 5)
    draw.set_color_rgb(255, 0, 0, stroke=True)
    draw.set_line_width(2)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __________
        __________
        ___RRRRR__
        ___RRRRR__
        __________
        __________
        __________
        __________
    ''')


def test_clip_even_odd():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(3, 3, 5, 6)
    draw.rectangle(4, 3, 2, 6)
    draw.clip(even_odd=True)
    draw.end()
    draw.move_to(0, 5)
    draw.line_to(10, 5)
    draw.set_color_rgb(255, 0, 0, stroke=True)
    draw.set_line_width(2)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __________
        __________
        ___R__RR__
        ___R__RR__
        __________
        __________
        __________
        __________
    ''')


def test_close():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.move_to(2, 2)
    draw.line_to(2, 8)
    draw.line_to(7, 8)
    draw.line_to(7, 2)
    draw.close()
    draw.set_color_rgb(0, 0, 255, stroke=True)
    draw.set_line_width(2)
    draw.stroke()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        _BBBBBBB__
        _BBBBBBB__
        _BB___BB__
        _BB___BB__
        _BB___BB__
        _BB___BB__
        _BBBBBBB__
        _BBBBBBB__
        __________
    ''')


def test_stroke_and_close():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.move_to(2, 2)
    draw.line_to(2, 8)
    draw.line_to(7, 8)
    draw.line_to(7, 2)
    draw.set_color_rgb(0, 0, 255, stroke=True)
    draw.set_line_width(2)
    draw.stroke_and_close()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        _BBBBBBB__
        _BBBBBBB__
        _BB___BB__
        _BB___BB__
        _BB___BB__
        _BB___BB__
        _BBBBBBB__
        _BBBBBBB__
        __________
    ''')


def test_fill_stroke_and_close():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.move_to(2, 2)
    draw.line_to(2, 8)
    draw.line_to(7, 8)
    draw.line_to(7, 2)
    draw.set_color_rgb(255, 0, 0)
    draw.set_color_rgb(0, 0, 255, stroke=True)
    draw.set_line_width(2)
    draw.fill_stroke_and_close()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        _BBBBBBB__
        _BBBBBBB__
        _BBRRRBB__
        _BBRRRBB__
        _BBRRRBB__
        _BBRRRBB__
        _BBBBBBB__
        _BBBBBBB__
        __________
    ''')


def test_push_pop_state():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(2, 2, 5, 6)
    draw.push_state()
    draw.rectangle(4, 4, 2, 2)
    draw.set_color_rgb(255, 0, 0)
    draw.pop_state()
    draw.fill()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __________
        __________
    ''')


def test_types():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(2, 2.0, '5', b'6')
    draw.set_line_width(2.3456)
    draw.fill()
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __________
        __________
    ''')


def test_compress():
    document = pydyf.PDF()

    draw = pydyf.Stream()
    draw.rectangle(2, 2, 5, 6)
    draw.fill()
    assert b'2 2 5 6' in draw.data

    draw = pydyf.Stream(compress=True)
    draw.rectangle(2, 2, 5, 6)
    draw.fill()
    assert b'2 2 5 6' not in draw.data
    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
    }))

    assert_pixels(document, '''
        __________
        __________
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __KKKKK___
        __________
        __________
    ''')


def test_text():
    document = pydyf.PDF()

    font = pydyf.Dictionary({
        'Type': '/Font',
        'Subtype': '/Type1',
        'Name': '/F1',
        'BaseFont': '/Helvetica',
        'Encoding': '/MacRomanEncoding',
    })
    document.add_object(font)

    draw = pydyf.Stream()
    draw.begin_text()
    draw.set_font_size('F1', 200)
    draw.set_text_matrix(1, 0, 0, 1, -20, 5)
    draw.show_text(pydyf.String('l'))
    draw.show_text(pydyf.String('É'))
    draw.end_text()

    document.add_object(draw)

    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'Contents': draw.reference,
        'MediaBox': pydyf.Array([0, 0, 10, 10]),
        'Resources': pydyf.Dictionary({
            'ProcSet': pydyf.Array(['/PDF', '/Text']),
            'Font': pydyf.Dictionary({'F1': font.reference}),
        }),
    }))

    assert_pixels(document, '''
        KKKKKKKKKK
        KKKKKKKKKK
        KKKKKKKKKK
        KKKKKKKKKK
        KKKKKKKKKK
        zzzzzzzzzz
        __________
        __________
        __________
        __________
    ''')


@pytest.mark.parametrize('compress', [False, True])
def test_no_identifier(compress):
    document = pydyf.PDF()
    pdf = io.BytesIO()
    document.write(pdf, compress=compress, identifier=False)
    assert re.search(
        b'/ID \\[\\((?P<hash>[0-9a-f]{32})\\) \\((?P=hash)\\)\\]',
        pdf.getvalue()
    ) is None


@pytest.mark.parametrize('compress', [False, True])
def test_default_identifier(compress):
    document = pydyf.PDF()
    pdf = io.BytesIO()
    document.write(pdf, compress=compress, identifier=True)
    assert re.search(
        b'/ID \\[\\((?P<hash>[0-9a-f]{32})\\) \\((?P=hash)\\)\\]',
        pdf.getvalue()
    ) is not None


@pytest.mark.parametrize('compress', [False, True])
def test_custom_identifier(compress):
    document = pydyf.PDF()
    pdf = io.BytesIO()
    document.write(pdf, compress=compress, identifier=b'abc')
    assert re.search(
        b'/ID \\[\\(abc\\) \\(([0-9a-f]{32})\\)\\]',
        pdf.getvalue()
    ) is not None


def test_version():
    document = pydyf.PDF()
    pdf = io.BytesIO()
    document.write(pdf, version=b'2.0')
    assert b'2.0' in pdf.getvalue()


def test_string_encoding():
    assert pydyf.String('abc').data == b'(abc)'
    assert pydyf.String('déf').data == b'<feff006400e90066>'
    assert pydyf.String('♡').data == b'<feff2661>'
    assert pydyf.String('\\abc').data == b'(\\\\abc)'
    assert pydyf.String('abc(').data == b'(abc\\()'
    assert pydyf.String('ab)c').data == b'(ab\\)c)'


def _build_encrypted(user_password='', owner_password='owner', permissions=-4):
    document = pydyf.PDF()
    content = pydyf.Stream([b'BT 10 100 Td (SecretContent) Tj ET'])
    document.add_object(content)
    document.add_page(pydyf.Dictionary({
        'Type': '/Page',
        'Parent': document.pages.reference,
        'MediaBox': pydyf.Array([0, 0, 200, 200]),
        'Contents': content.reference,
    }))
    document.info['Title'] = pydyf.String('Secret Title')
    output = io.BytesIO()
    encryption = pydyf.Encryption(
        owner_password=owner_password, user_password=user_password,
        permissions=permissions)
    document.write(output, encryption=encryption)
    return output.getvalue(), encryption, content


def test_encryption_structure():
    data, encryption, _ = _build_encrypted()
    assert b'/Encrypt' in data
    assert b'/Filter /Standard' in data
    assert b'/ID [' in data
    # O and U are 32 bytes, the file key is 16 bytes (128-bit, revision 3).
    assert len(encryption.owner_entry) == 32
    assert len(encryption.user_entry) == 32
    assert len(encryption.key) == 16


def test_encryption_roundtrip():
    # An empty user password must let the document open, and the per-object key
    # must decrypt the content stream back to its plaintext.
    data, encryption, content = _build_encrypted(user_password='')
    object_key = encryption.object_key(content.number, content.generation)
    match = re.search(
        rb'%d 0 obj.*?stream\n(.*?)\nendstream' % content.number, data, re.S)
    decrypted = pydyf._rc4(object_key, match.group(1))
    assert b'SecretContent' in decrypted


def test_encryption_key_derivation():
    # Re-deriving the file key from the (empty) user password and the stored
    # O/P/ID must reproduce the encryption key (Algorithm 2).
    from hashlib import md5
    _, encryption, _ = _build_encrypted(user_password='')
    digest = md5()
    digest.update(pydyf._pad_password(''))
    digest.update(encryption.owner_entry)
    digest.update(encryption.permissions.to_bytes(4, 'little', signed=True))
    digest.update(encryption.id)
    key = digest.digest()
    for _ in range(50):
        key = md5(key[:16]).digest()
    assert key[:16] == encryption.key


def test_aes_block_vector():
    # FIPS-197 known-answer test for the AES-128 block cipher.
    key = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
    plaintext = bytes.fromhex('00112233445566778899aabbccddeeff')
    expected = bytes.fromhex('69c4e0d86a7b0430d8cdb78070b4c55a')
    cipher = pydyf._aes_encrypt_block(plaintext, pydyf._aes_expand_key(key))
    assert cipher == expected


def test_aes_encryption_structure():
    data = _build_encrypted()[0]  # default rc4
    assert b'/AESV2' not in data
    document = pydyf.PDF()
    content = pydyf.Stream([b'BT 10 100 Td (AesContent) Tj ET'])
    document.add_object(content)
    document.add_page(pydyf.Dictionary({
        'Type': '/Page', 'Parent': document.pages.reference,
        'MediaBox': pydyf.Array([0, 0, 200, 200]),
        'Contents': content.reference}))
    output = io.BytesIO()
    document.write(output, encryption=pydyf.Encryption(method='aes'))
    aes = output.getvalue()
    assert b'/AESV2' in aes
    assert b'/V 4' in aes
    assert b'/StmF /StdCF' in aes
