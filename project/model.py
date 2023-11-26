import pymysql
from pprint import pprint

class Database:
    def connect(self):
        return pymysql.connect(host='localhost', user='root', password='', database='quiz_maker', charset='utf8mb4')
    
    # return all questions and answers if id is None
    # else return question and answer with "question_id"
    def read_question(self, question_id):
        con = self.connect()
        cursor = con.cursor()

        # fetch questions
        try:
            if question_id is None:
                cursor.execute('SELECT * FROM questions')
            else:
                cursor.execute('SELECT * FROM questions where question_id = %s',(question_id,))
            questions = cursor.fetchall()
        except Exception as e:
            print(e)

        # fetch answers
        try:
            if question_id is None:
                cursor.execute('SELECT * FROM answers')
            else:
                cursor.execute('SELECT * FROM answers where question_id = %s',(question_id,))
            answers = cursor.fetchall()
        except Exception as e:
            print(e)

        # convert tuple into list
        questions = [list(question) for question in questions]

        for question in questions:
            choices = []
            for answer in answers:
                if question[0] == answer[0]:
                    choices.append(answer)
            question.append(choices)

        return questions

        # returned questions look like these
        # [[11, 'How many letters in alphabet?', [(11, '26', 'Y'), (11, '31', 'N'), (11, '21', 'N')]],
        #  [12, 'The most popular desktop operating system is?', [(12, 'Mac OS', 'N'), (12, 'Windows', 'Y')]]]
        

    # get last auto increment value on questions table
    # works by assuming questions table not empty
    def last_auto_increment_value(self):    
        con = self.connect()
        cursor = con.cursor()
        try: 
            cursor.execute('SELECT question_id FROM questions ORDER BY question_id DESC LIMIT 1')
            row = cursor.fetchone()
            print(row[0])
        except Exception as e:
            print(e)
            return -1
        finally:
            con.close()

        if row is not None:
            return row[0]   # return last auto increment question_id
        else:
            return -1

    # insert a question and its answers
    # @param
    # question : str
    # choices : looks like this [['choice 1', 'N'], ['choice 2', 'Y'], ...]
    def insert_question(self, question, choices):
        con = self.connect()
        cursor = con.cursor()

        # insert into questions table
        try:
            cursor.execute('INSERT INTO questions(question) VALUES(%s)',
                                (question,))
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
            return False

        # insert into answers table
        try:
            question_id = self.last_auto_increment_value()
            for i in range(len(choices)):
                cursor.execute('INSERT INTO answers(question_id, choice, is_answer) VALUES(%s, %s, %s)',
                            (question_id, choices[i][0], choices[i][1]))
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            cursor.close()
            con.close()

        return True


    def delete_question(self, question_id):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute('DELETE FROM questions WHERE question_id = %s', 
                        (question_id,))
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            cursor.close()
            con.close()

        return True

    def edit_question(self, question_id, question, choices):
        con = Database.connect(self)
        cursor = con.cursor()
        # edit question in questions table
        try:
            cursor.execute('UPDATE questions SET question = %s WHERE question_id = %s', 
                            (question, question_id))
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
            return False

        # delete choices in answers table
        try:
            cursor.execute('DELETE FROM answers WHERE question_id = %s', (question_id,))
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
            return False

        # insert into answers table
        try:
            for i in range(len(choices)):
                cursor.execute('INSERT INTO answers(question_id, choice, is_answer) VALUES(%s, %s, %s)',
                            (question_id, choices[i][0], choices[i][1]))
            con.commit()
        except Exception as e:
            print(e)
            con.rollback()
            return False
        finally:
            cursor.close()
            con.close()

        return True
