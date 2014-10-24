import java.io.IOException;

public class Test {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {

		//make an Eliza object
		Eliza e = new Eliza();
		//introduces Eliza
		e.welcomeMessage();
		//starts the program
		e.start();

	}

}
