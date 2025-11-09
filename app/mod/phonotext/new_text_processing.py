''' module for working with phonotext by the chain of responsibility '''

from collections.abc import Callable
import abc
from typing import Iterable, overload
import yaml


ZERO_SPACE = '\u200B'

STAT = [
        (frozenset('ст') ,'ст', 5.520299027089752),
        (frozenset('рт') ,'рт', 3.9041440925190565),
        (frozenset('кт') ,'кт', 3.700607029682931),
        (frozenset('кс') ,'кс', 3.685935565680993),
        (frozenset('нт') ,'нт', 3.6181787510506047),
        (frozenset('лс') ,'лс', 3.4066146873401784),
        (frozenset('вт') ,'вт', 3.396655959868601),
        (frozenset('вс') ,'вс', 3.129480694521162),
        (frozenset('нс') ,'нс', 3.0619972793019348),
        (frozenset('лт') ,'лт', 2.9884838227091373),
        (frozenset('тч') ,'тч', 2.7029794262818374),
        (frozenset('рс') ,'рс', 2.606627516064834),
        (frozenset('пр') ,'пр', 2.5962102239431837),
        (frozenset('кр') ,'кр', 2.561106077678492),
        (frozenset('кн') ,'кн', 2.5557810671153383),
        (frozenset('пт') ,'пт', 2.4053949044623306),
        (frozenset('кл') ,'кл', 2.3173750445079437),
        (frozenset('пс') ,'пс', 2.1533159375289515),
        (frozenset('лн') ,'лн', 2.0475587139195657),
        (frozenset('лп') ,'лп', 1.9173091040680041),
        (frozenset('вн') ,'вн', 1.8294587103360653),
        (frozenset('вк') ,'вк', 1.8263973704604777),
        (frozenset('нч') ,'нч', 1.7470574406754997),
        (frozenset('лч') ,'лч', 1.6324620700528),
        (frozenset('нр') ,'нр', 1.6283706871845904),
        (frozenset('кп') ,'кп', 1.6085164358236366),
        (frozenset('сч') ,'сч', 1.5969582301055887),
        (frozenset('мс') ,'мс', 1.5807459578200493),
        (frozenset('вл') ,'вл', 1.572892779187498),
        (frozenset('нп') ,'нп', 1.5498214575074492),
        (frozenset('вр') ,'вр', 1.5094737805437959),
        (frozenset('мн') ,'мн', 1.5070134006154712),
        (frozenset('мт') ,'мт', 1.4720810844433736),
        (frozenset('рч') ,'рч', 1.3449898873387365),
        (frozenset('км') ,'км', 1.1448959479927379),
        (frozenset('вч') ,'вч', 1.1416178727522592),
        (frozenset('лр') ,'лр', 1.060199393462806),
        (frozenset('вп') ,'вп', 1.0148090679532447),
        (frozenset('пч') ,'пч', 0.9366281463163952),
        (frozenset('кч') ,'кч', 0.9091197426244838),
        (frozenset('jн') ,'jн', 0.8806893538549048),
        (frozenset('jт') ,'jт', 0.8625725869764448),
        (frozenset('лм') ,'лм', 0.8483845048192463),
        (frozenset('jк') ,'jк', 0.8188201715334538),
        (frozenset('мр') ,'мр', 0.7794800388053363),
        (frozenset('jс') ,'jс', 0.7482144418056329),
        (frozenset('мп') ,'мп', 0.687289618035195),
        (frozenset('вм') ,'вм', 0.6754263202497546),
        (frozenset('мч') ,'мч', 0.6590536365897268),
        (frozenset('jп') ,'jп', 0.5769597003364467),
        (frozenset('jр') ,'jр', 0.4917480231194904),
        (frozenset('jч') ,'jч', 0.4571093802966799),
        (frozenset('jв') ,'jв', 0.4340063976255217),
        (frozenset('jл') ,'jл', 0.40533896926454904),
        (frozenset('тц') ,'тц', 0.30565230461660814),
        (frozenset('jм') ,'jм', 0.24134987662233412),
        (frozenset('рц') ,'рц', 0.18449840312187302),
        (frozenset('нц') ,'нц', 0.17496443296473105),
        (frozenset('кц') ,'кц', 0.16727171113923367),
        (frozenset('сц') ,'сц', 0.1600195681748873),
        (frozenset('вц') ,'вц', 0.13762826185939417),
        (frozenset('лц') ,'лц', 0.13742492359432004),
        (frozenset('пц') ,'пц', 0.11837277591511969),
        (frozenset('jц') ,'jц', 0.07005670608653768),
        (frozenset('мц') ,'мц', 0.05272835254345556),
        (frozenset('цч') ,'цч', 0.035375151517330276)
    ]

class Letter:...

class Word:
    '''save first letter of word and word number in text'''

    def __init__(self, number: int, start_letter: Letter):
        self.number: int = number
        self.start_letter: Letter = start_letter


class LetterPosition:
    ''' difrent positions of letter in text'''

    def __init__(self, **config):
        self.text = 0
        self.syllab = 0
        self.word_start = 0
        self.word_end = 0
        self.last_word_in_line = 0


class Letter():
    ''' class for letter in text'''

    def __init__(self, char: str, visual_char: str | None = None):
        self.origin: str = char if visual_char is None else visual_char
        self.technic: str = char
        self.printable: str = char
        self.is_consonant: bool = False
        self.is_volve: bool = False
        self.is_accent = False
        self.word: Word | None = None
        self.position = LetterPosition()
        self.next_letter: (Letter | None) = None

    def __str__(self):
        return self.origin + '(' + "".join([self.technic, self.printable]) + ')'

    def __repr__(self):
        return "'".join([
            self.origin,
            self.technic,
            self.printable,
            'C' if self.is_consonant else '-',
            'V' if self.is_volve else '-',
            str(self.position.syllab),
            str(self.position.text),
            str(self.word.number)
        ])

    def __iter__(self):
        while self is not None:
            yield self
            self = self.next_letter

    def volves(self):
        '''iterator by volves'''
        while self is not None:
            if self.is_volve:
                yield self
            self = self.next_letter

    def consonants(self):
        '''iterator by consonants'''
        while self is not None:
            if self.is_consonant:
                yield self
            self = self.next_letter

    def insert(self, l: Letter):
        """Insert letter L after current"""
        l.next_letter = self.next_letter
        self.next_letter = l

    def remove_next(self):
        """Remove next letter"""
        tmp = self.next_letter
        self.next_letter = self.next_letter.next_letter
        del tmp

    def join_next(self):
        self.origin += self.next_letter.origin
        self.printable += self.next_letter.printable
        self.technic += self.next_letter.technic
        self.remove_next()



Syllab_potencial = list[Letter]


class Combination:
    """List of letter in one combination and it's power"""

    def __init__(self, lst: list[Letter], pwr: float):
        self.list: list[Letter] = lst
        self.power: float = pwr

    def __iter__(self):
        yield from self.list

    def __getitem__(self, id) -> Letter:
        return self.list[id]

    def __setitem__(self, id: int, letter: Letter):
        self.list[id] = letter

    def __repr__(self):
        return ''.join(map(lambda x: x.printable, self.list))

    def get_printable(self) -> str:
        return ''.join((x.printable for x in self.list))


class Repeat:
    """List of combination in one chain of sound repeats"""
    def __init__(self, letters: frozenset):
        self.count: int = 0
        self.power: float = .0
        self.letters: list[Letter] = []
        self.combs: list[Combination] = []
        self._words: frozenset = letters

    def __iter__(self):
        yield from self.combs

    def __repr__(self):
        return repr(self.combs)


class Phonotext():
    ''' class, that looks on text as a linked list of Letters '''

    def __init__(self, text:str, visual_text=None):
        self.count_letters = 0

        if visual_text is None:
            letters = iter(text.lower())
            self.text: Letter = Letter(next(letters))
            l = self.text
            for x in letters:
                l.next_letter = Letter(x)
                l = l.next_letter
                self.count_letters += 1
        else:
            letters = iter(text.lower())
            visletters = iter(visual_text)
            self.text: Letter = Letter(next(letters), next(visletters))
            l = self.text
            for x, y in zip(letters, visletters):
                l.next_letter = Letter(x, y)
                l = l.next_letter
                self.count_letters += 1

        # self.last_letter = l
        self.repeats: list[tuple[frozenset, Repeat]] = list()
        self.SP: list[Syllab_potencial] = list()
        self.combs: list[list[Combination]] = list()
        self.count_words = 0

    def count_letters(self) -> tuple[int, int]:
        count_symbols = count_volves = 0
        for symb in self.text:
            if symb.is_consonant:
                count_symbols += 1
            if symb.is_volve and symb.printable not in ["--endl", '\n']:
                count_volves += 1
                count_symbols += 1
        return count_volves, count_symbols

    def get_origin(self) -> str:
        return ''.join([x.origin for x in self.text])

    def get_technic(self) -> str:
        return ''.join((x.technic for x in self.text))

    def get_printable(self) -> str:
        return ''.join((x.printable for x in self.text))

    def __repr__(self) -> str:
        return ''.join((repr(x) for x in self.text))


class AbstractEvent(abc.ABC):
    '''
    Abstract event
    '''
    @abc.abstractmethod
    def __init__(self):
        pass


class TextProcessorHandler():
    def __init__(self, succesor=None):
        self.__succesor = succesor

    def handle(self, obj: Phonotext, conf: AbstractEvent):
        if self.__succesor is not None:
            return self.__succesor.handle(obj, conf)


class SameEvent(AbstractEvent):
    def __init__(self, rules):
        self.rules = dict()
        for r in rules:
            for ch in r:
                self.rules[ch] = r[0]


class SameProcessor(TextProcessorHandler):
    def handle(self, obj, conf):
        if isinstance(conf, SameEvent):
            for l in obj.text:
                l.technic = conf.rules.get(l.printable, ZERO_SPACE)
                if l.technic in {ZERO_SPACE, '|'}:
                    l.printable = l.technic
        else:
            super().handle(obj, conf)


class NumberEvent(AbstractEvent):
    def __init__(self, volves: Iterable[str], consonants: Iterable[str], alphabet:Iterable[str]):
        self.volves = set(volves)
        self.consonants = set(consonants)
        self.letters = set(alphabet)


class NumberProcessor(TextProcessorHandler):
    def handle(self, obj, conf):
        if isinstance(conf, NumberEvent):
            i = 0
            j = 1
            obj.count_words = 1
            zero_word = Word(0, None)
            last_word = cur_word = Word(obj.count_words, obj.text)
            num = 1
            space = False

            for i, letter in enumerate(obj.text):
                letter.position.text = i
                letter.word = cur_word
                letter.position.word_start = num

                space = letter.technic not in conf.letters
                if space:
                    obj.count_words += 1
                    letter.word = zero_word
                    l = letter.next_letter
                    while l is not None and l.technic not in conf.letters:
                        l = l.next_letter
                        letter.join_next()
                        obj.count_letters -= 1


                    for i, l in enumerate(cur_word.start_letter):
                        if l is letter: break
                        l.position.word_end = num - i

                    last_word = cur_word
                    cur_word = Word(obj.count_words, letter.next_letter)

                    for w in last_word.start_letter:
                        if w.word.number == 0: break
                        num -= 1
                        w.position.word_end = num
                    num -= 1

                if "\n" in letter.technic:
                    for w in last_word.start_letter:
                        if w.word.number == 0: break
                        w.position.last_word_in_line = 1

                if letter.printable in conf.volves:
                    letter.is_volve = True
                    j += 1
                if letter.printable in conf.consonants:
                    letter.is_consonant = True
                letter.position.syllab = j
                i += 1
                num += 1
        else:
            super().handle(obj, conf)


class JoinEvent(AbstractEvent):
    def __init__(self, rules: list[str]):
        self.rules: dict[str, str] = {}
        for a in rules:
            self.rules[a[0]] = a


class JoinProcessor(TextProcessorHandler):
    def handle(self, obj, conf):
        if isinstance(conf, JoinEvent):
            for letter in obj.text:
                if letter.next_letter is None: break
                tmp_a = letter.origin
                tmp_b = letter.next_letter.origin
                if tmp_a in conf.rules:
                    if tmp_a + tmp_b == conf.rules[tmp_a]:
                        letter.join_next()
                    if tmp_b == "\u0301":  # accent  1100 1100 1000 0001
                        letter.printable = tmp_a + tmp_b
                        letter.is_accent = True
                        letter.remove_next()
                    if tmp_b == "\u0484":
                        letter.remove_next()
        else:
            super().handle(obj, conf)


class ModifyEvent(AbstractEvent):
    def __init__(self, rules:dict[str, str]):
        self.rules:dict[str, dict[str, str]] = dict()
        for a in rules:
            if a[0] not in self.rules: self.rules[a[0]] = dict()
            self.rules[a[0]][a[1]] = rules[a]


class ModifyProcessor(TextProcessorHandler):
    def handle(self, obj, conf):
        if isinstance(conf, ModifyEvent):
            for letter in obj.text:
                if letter.next_letter is None: break
                tmp_a = letter.origin
                tmp_b = letter.next_letter.origin
                if tmp_a in conf.rules:
                    if tmp_b in conf.rules[tmp_a]:
                        tmp_c = conf.rules[tmp_a][tmp_b]
                        letter.insert(Letter(ZERO_SPACE))
                        letter.printable = tmp_c[0]
                        letter.next_letter.printable = tmp_c[1]
                        letter.next_letter.next_letter.printable = tmp_c[2]
        else:
            super().handle(obj, conf)


class SPmaxEvent(AbstractEvent):
    def __init__(self):
        pass


class SPmaxProcessor(TextProcessorHandler):
    def handle(self, obj, conf):
        if isinstance(conf, SPmaxEvent):
            iterator = obj.text.volves()
            obj.SP.clear()
            start = obj.text
            middle = next(iterator)
            i = 0
            for end in iterator:
                obj.SP.append(list())
                for x in start:
                    if x is end: break
                    obj.SP[-1].append(x)
                i += 1
                start = middle.next_letter
                middle = end
                if end.origin == "\n":
                    start = middle.next_letter
                    middle = next(iterator)
                if sum(1 if x.is_consonant or x.is_volve else 0 for x in obj.SP[-1]) == 0:
                    obj.SP.pop()
        else:
            super().handle(obj, conf)


class CombinationsEvent(AbstractEvent):
    def __init__(self, max_cons, filter_combination):
        self.max_cons = max_cons
        self.filter_combination = filter_combination


class CombinationsProcessor(TextProcessorHandler):

    def combinations(self,
                     s: Syllab_potencial,
                     N: int,
                     filter_combination: Callable[[list[int], list[int], str, bytes], tuple[bool, float]]
                     ) -> list[Combination]:
        N += 1
        pos_vol = list(finder_volv(s))
        pos_cons = list(finder_cons(s))
        indexes = []
        cons_num = 1 << len(pos_cons)
        for i in range(cons_num):
            tmp = bin(cons_num | i)[2:]
            if tmp.count('1') == N:
                indexes.append([])
                for j in range(1, len(tmp)):
                    if tmp[j] == '1':
                        indexes[-1].append(j - 1)
        res = []
        for tmp in indexes:
            tmp = [pos_cons[j] for j in tmp] + pos_vol
            tmp.sort()
            if len({s[i].technic for i in tmp}) < N:
                continue
            lst = ''.join([s[i].technic for i in range(tmp[0], tmp[-1] + 1)])
            lst += '-' + ''.join([s[i].printable for i in tmp])
            positions = b''.join([s[i].position.word_start.to_bytes(1, "little") for i in tmp])
            flt = filter_combination(tmp, pos_vol, lst, positions)
            if flt[0]:
                # for i in tmp:
                #     s[i].pwr += flt[1] / N
                res.append(Combination([s[i] for i in tmp], flt[1]))
        return res

    def handle(self, obj, conf):
        if isinstance(conf, CombinationsEvent):
            obj.combs.clear()
            for syllab in obj.SP:
                obj.combs.append(self.combinations(syllab, conf.max_cons, conf.filter_combination))
        else:
            super().handle(obj, conf)


def list_update(a: Combination, b: Combination):
    if b.power > a.power:
        a.power = b.power
    for el in b:
        if a[0].position.text > el.position.text:
            a.list.insert(0, el)
            continue
        for i in range(len(a.list) - 1):
            if a[i].position.text < el.position.text < a[i + 1].position.text:
                a.list.insert(i + 1, el)
        if a[-1].position.text < el.position.text:
            a.list.append(el)


class RepeatEvent(AbstractEvent):
    def __init__(self):
        pass


class RepeatProcessor(TextProcessorHandler):

    def handle(self, obj, conf):
        if isinstance(conf, RepeatEvent):
            res: dict[frozenset, Repeat] = dict()
            for n_syll in range(len(obj.combs)):
                for comb in obj.combs[n_syll]:
                    tmp = frozenset((l.technic for l in comb if l.is_consonant))
                    if tmp not in res: res[tmp] = Repeat(tmp)
                    res[tmp].count += 1
                    res[tmp].power += comb.power
                    res[tmp].letters.extend(comb)
                    if (len(res[tmp].combs) > 0 and
                        res[tmp].combs[-1][-1].position.text >= comb[0].position.text):
                        list_update(res[tmp].combs[-1], comb)
                    else:
                        res[tmp].combs.append(comb)
            obj.repeats = list(res.items())
            obj.repeats.sort(key=lambda x: x[1].power, reverse=True)


        else:
            super().handle(obj, conf)


class RepeatRecountEvent(AbstractEvent):
    def __init__(self):
        pass


class RepeatRecountProcessor(TextProcessorHandler):
    @staticmethod
    def get_pwr(a:Letter, b:Letter):
        if a.technic != b.technic:
            return 0

        dist = b.position.syllab - a.position.syllab
        if dist < 1:
            return 0

        pwr = 0
        mul = 1
        dist_w = b.word.number - a.word.number

        pwr = 1 / dist + 1 / (dist_w + 2)
        if a.origin == b.origin and a.is_consonant:
            mul += 1
        mul *= 1 / (1 + a.position.word_start + b.position.word_start)
        # if a.w_pos[0] == b.w_pos[0] and a.w_pos[0] != 0:
        #     mul += 1
        # if a.w_pos[1] == b.w_pos[1] and a.w_pos[1] != 0:
        #     mul += 0
        return pwr * mul  # * 2 / max(1, b.w_pos[0] - b.w_pos[1] + a.w_pos[0] - a.w_pos[1])

    @staticmethod
    def get_pwr_combs(a:Combination, b:Combination):
        pwr = 0
        for i in range(len(a.list)):
            for j in range(len(b.list)):
                pwr += RepeatRecountProcessor.get_pwr(a[i], b[j])

        mul_1 = 1
        mul_2 = 1
        for i in range(len(a.list) - 1):
            mul_1 *= a[i + 1].position.text - a[i].position.text
        for i in range(len(b.list) - 1):
            mul_2 *= b[i + 1].position.text - b[i].position.text

        mul = 10 * a.power * b.power * (1 + a[-1].position.last_word_in_line + b[-1].position.last_word_in_line)

        # dist = (a[0][0].number + a[0][1].number + a[0][2].number) // 3 - (b[0][0].number + b[0][1].number + b[0][2].number) // 3

        pwr *= 1 / (mul_1 + 1) + 1 / (mul_2 + 1)

        # if dist < 3:
        #     pwr *= 0.001
        # else:
        #     pwr *= 1/dist

        return pwr * mul

    def handle(self, obj, conf):
        if isinstance(conf, RepeatRecountEvent):
            for x, data in obj.repeats:
                data.count = 1
                last = data.combs[0]
                for y in data.combs:
                    if y[0].position.text - last[-1].position.text > 0:
                        data.count += 1
                    last = y

            for _, rep in obj.repeats:
                pwr = 0

                for i in range(len(rep.combs) - 1):
                    for j in range(i, len(rep.combs)):
                        pwr += self.get_pwr_combs(rep.combs[i], rep.combs[j])
                        if rep.combs[j][0].word.number - rep.combs[i][0].word.number > 50: break
                rep.power = pwr
            obj.repeats.sort(key=lambda x: x[1].power, reverse=True)

        else:
            super().handle(obj, conf)


def finder_volv(data:list[Letter]):
    '''
    find volv generator
    '''
    curr = 0
    last = len(data)
    while curr < last:
        if data[curr].is_volve:
            yield curr
        curr += 1
    # yield curr


def finder_cons(data:list[Letter]):
    '''
    find cons generator
    '''
    curr = 0
    last = len(data)
    while curr < last:
        if data[curr].is_consonant:
            yield curr
        curr += 1
    # yield curr


def get_filter_com_rus(min_pwr, max_pwr):

    def rus_filter_comb(indexes: list[int], vol_pos: list[int], txt: str, positions: bytes):

        if len(set(txt[-3:])) < 3:
            return False, 0
        if indexes[0] == vol_pos[0]:
            pwr = 2
        elif indexes[2] == vol_pos[0]:
            pwr = 1
        else:
            pwr = 3
        pwr += 5 if indexes[2] - indexes[0] - txt.count('|') == 2 else 0
        pwr += 0 if txt.find('|') != -1 else 2
        pwr += 0 if txt.find('й', -3) != -1 else 4
        pwr += 1 if positions.find(b'\x01', -3) != -1 else 0
        pwr /= 15
        return min_pwr <= pwr <= max_pwr, pwr

    return rus_filter_comb


def load_config(filename):
    '''
    load yaml file from filename
    '''
    with open(filename, 'r', encoding="utf-8") as stream:
        try:
            config = yaml.load(stream, Loader=yaml.SafeLoader)

            return [
                ModifyEvent(config['modifications']),
                JoinEvent(config['as_one']),
                NumberEvent(config['volves'], config['consonants'], config['alphabet']),
                SameEvent(list(config['alphabet']) + config['as_same']),
                SPmaxEvent(),
                CombinationsEvent(2, get_filter_com_rus(0, 11)),
                RepeatEvent(),
                RepeatRecountEvent(),
            ]
            # return config
        except yaml.YAMLError as exc:
            print(f'ERROR {exc}')

        return None


CONFIG = {
    'rus' : load_config("./app/mod/text_mikl/russian.yaml"),
    'eng' : load_config("./app/mod/text_mikl/english.yaml"),
    'latin' : load_config("./app/mod/text_mikl/latin.yaml")
}

PROCESSOR = TextProcessorHandler()
PROCESSOR = ModifyProcessor(PROCESSOR)
PROCESSOR = SameProcessor(PROCESSOR)
PROCESSOR = JoinProcessor(PROCESSOR)
PROCESSOR = SPmaxProcessor(PROCESSOR)
PROCESSOR = CombinationsProcessor(PROCESSOR)
PROCESSOR = NumberProcessor(PROCESSOR)
PROCESSOR = RepeatProcessor(PROCESSOR)
PROCESSOR = RepeatRecountProcessor(PROCESSOR)

if __name__ =="__main__":

    text = """— Скажи-ка, дядя, ведь не даром
Москва, спаленная пожаром,
Французу отдана?
Ведь были ж схватки боевые,
Да, говорят, еще какие!
Недаром помнит вся Россия
Про день Бородина!
— Да, были люди в наше время,
Не то, что нынешнее племя:
Богатыри — не вы!
Плохая им досталась доля:
Немногие вернулись с поля...
Не будь на то господня воля,
Не отдали б Москвы!
Мы долго молча отступали,
Досадно было, боя ждали,
Ворчали старики:
«Что ж мы? на зимние квартиры?
Не смеют, что ли, командиры
Чужие изорвать мундиры
О русские штыки?»
И вот нашли большое поле:
Есть разгуляться где на воле!
Построили редут.
У наших ушки на макушке!
Чуть утро осветило пушки
И леса синие верхушки —
Французы тут как тут.
Забил заряд я в пушку туго
И думал: угощу я друга!
Постой-ка, брат мусью!
Что тут хитрить, пожалуй к бою;
Уж мы пойдем ломить стеною,
Уж постоим мы головою
За родину свою!
Два дня мы были в перестрелке.
Что толку в этакой безделке?
Мы ждали третий день.
Повсюду стали слышны речи:
«Пора добраться до картечи!»
И вот на поле грозной сечи
Ночная пала тень.
Прилег вздремнуть я у лафета,
И слышно было до рассвета,
Как ликовал француз.
Но тих был наш бивак открытый:
Кто кивер чистил весь избитый,
Кто штык точил, ворча сердито,
Кусая длинный ус.
И только небо засветилось,
Все шумно вдруг зашевелилось,
Сверкнул за строем строй.
Полковник наш рожден был хватом:
Слуга царю, отец солдатам...
Да, жаль его: сражен булатом,
Он спит в земле сырой.
И молвил он, сверкнув очами:
«Ребята! не Москва ль за нами?
Умремте ж под Москвой,
Как наши братья умирали!»
И умереть мы обещали,
И клятву верности сдержали
Мы в Бородинский бой.
Ну ж был денек! Сквозь дым летучий
Французы двинулись, как тучи,
И всё на наш редут.
Уланы с пестрыми значками,
Драгуны с конскими хвостами,
Все промелькнули перед нам,
Все побывали тут.
Вам не видать таких сражений!
Носились знамена, как тени,
В дыму огонь блестел,
Звучал булат, картечь визжала,
Рука бойцов колоть устала,
И ядрам пролетать мешала
Гора кровавых тел.
Изведал враг в тот день немало,
Что значит русский бой удалый,
Наш рукопашный бой!..
Земля тряслась — как наши груди;
Смешались в кучу кони, люди,
И залпы тысячи орудий
Слились в протяжный вой...
Вот смерклось. Были все готовы
Заутра бой затеять новый
И до конца стоять...
Вот затрещали барабаны —
И отступили басурманы.
Тогда считать мы стали раны,
Товарищей считать.
Да, были люди в наше время,
Могучее, лихое племя:
Богатыри — не вы.
Плохая им досталась доля:
Немногие вернулись с поля.
Когда б на то не Божья воля,
Не отдали б Москвы!"""

    test_conf = load_config("russian.yaml")

    text = Phonotext(text)
    test_conf[5] = CombinationsEvent(2, get_filter_com_rus(0, 1))
    for test in test_conf:
        PROCESSOR.handle(text, test)
    print(repr(text.repeats))