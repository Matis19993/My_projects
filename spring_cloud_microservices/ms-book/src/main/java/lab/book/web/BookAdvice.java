package lab.book.web;

import lab.book.MsBookException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

@ControllerAdvice
@Slf4j
public class BookAdvice {

    @ExceptionHandler(MsBookException.class)
    ResponseEntity<String> handleMsBookException(MsBookException e){
        log.error("unhandled exception occured", e);
        return ResponseEntity.status(HttpStatus.I_AM_A_TEAPOT).body(e.getMessage());
    }

}
